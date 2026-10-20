"""Filigrane PDF : applique un filigrane répété sur un ou plusieurs PDF."""
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import fitz
except ImportError:
    fitz = None

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None


class FiligranePDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Filigrane PDF")
        resource_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        icon_png = resource_dir / "icon.png"
        if icon_png.exists():
            try:
                self._window_icon = tk.PhotoImage(file=str(icon_png))
                self.root.iconphoto(True, self._window_icon)
            except tk.TclError:
                pass
        if sys.platform == "win32":
            icon_ico = resource_dir / "icon.ico"
            if icon_ico.exists():
                self.root.iconbitmap(str(icon_ico))
        self.root.geometry("760x650")
        self.root.minsize(680, 560)
        self.root.configure(bg="#f4f6fa")

        self.pdf_paths = []
        self.watermark = tk.StringVar(value="CONFIDENTIEL")
        self.font_size = tk.IntVar(value=28)
        self.rotation = tk.IntVar(value=25)
        self.output_folder = tk.StringVar()
        self.status = tk.StringVar(value="Ajoutez un ou plusieurs fichiers PDF.")

        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fa")
        style.configure("TLabel", background="#f4f6fa", foreground="#20283a", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="#18233b")
        style.configure("Hint.TLabel", foreground="#65718a")
        style.configure("TButton", font=("Segoe UI", 10), padding=(11, 7))
        style.configure("Accent.TButton", background="#315efb", foreground="white", font=("Segoe UI", 10, "bold"))

        outer = ttk.Frame(self.root, padding=26)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Filigrane PDF", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Répétez un texte en diagonale sur chaque page et traitez plusieurs fichiers à la fois.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        files_header = ttk.Frame(outer)
        files_header.pack(fill="x")
        self.files_label = ttk.Label(files_header, text="PDF sélectionnés (0)")
        self.files_label.pack(side="left")
        ttk.Button(files_header, text="Ajouter des PDF…", command=self.add_pdfs).pack(side="right")
        ttk.Button(files_header, text="Vider la liste", command=self.clear_pdfs).pack(side="right", padx=(0, 8))

        list_frame = ttk.Frame(outer)
        list_frame.pack(fill="both", expand=True, pady=(8, 4))
        self.file_list = tk.Listbox(
            list_frame,
            height=7,
            selectmode=tk.EXTENDED,
            font=("Segoe UI", 10),
            bg="white",
            fg="#20283a",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d9deea",
            activestyle="none",
        )
        self.file_list.bind("<Delete>", self.remove_selected_pdfs)
        if DND_FILES is not None:
            self.file_list.drop_target_register(DND_FILES)
            self.file_list.dnd_bind("<<Drop>>", self.drop_pdfs)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_list.yview)

        self.file_list.configure(yscrollcommand=scrollbar.set)
        self.file_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        ttk.Label(
            outer,
            text="Glissez-déposez vos PDF dans la liste ci-dessus.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(0, 14))

        ttk.Label(outer, text="Texte du filigrane").pack(anchor="w")
        self.watermark_entry = ttk.Entry(outer, textvariable=self.watermark)
        self.watermark_entry.pack(fill="x", pady=(7, 14), ipady=6)

        options = ttk.Frame(outer)
        options.pack(fill="x", pady=(0, 16))
        ttk.Label(options, text="Taille").pack(side="left")
        ttk.Spinbox(options, from_=12, to=64, textvariable=self.font_size, width=6).pack(side="left", padx=(8, 20), ipady=3)
        ttk.Label(options, text="Inclinaison").pack(side="left")
        ttk.Spinbox(options, from_=-60, to=60, textvariable=self.rotation, width=6).pack(side="left", padx=(8, 6), ipady=3)
        ttk.Label(options, text="degrés", style="Hint.TLabel").pack(side="left")

        ttk.Label(outer, text="Dossier de destination").pack(anchor="w")
        output_row = ttk.Frame(outer)
        output_row.pack(fill="x", pady=(7, 15))
        ttk.Entry(output_row, textvariable=self.output_folder, state="readonly").pack(side="left", fill="x", expand=True, ipady=6)
        ttk.Button(output_row, text="Choisir…", command=self.choose_output_folder).pack(side="left", padx=(9, 0))

        ttk.Separator(outer).pack(fill="x", pady=(0, 14))

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x")
        ttk.Label(bottom, textvariable=self.status, style="Hint.TLabel").pack(side="left", fill="x", expand=True)
        ttk.Button(bottom, text="Créer les PDF filigranés", style="Accent.TButton", command=self.export_pdfs).pack(side="right")

    def add_pdfs(self):
        selected = filedialog.askopenfilenames(
            title="Choisir un ou plusieurs fichiers PDF",
            filetypes=[("Fichiers PDF", "*.pdf")],
        )
        self._add_pdf_paths(selected)

    def drop_pdfs(self, event):
        dropped_paths = self.root.tk.splitlist(event.data)
        self._add_pdf_paths(dropped_paths, from_drop=True)
        return "break"

    def _add_pdf_paths(self, filenames, from_drop=False):
        added = 0
        ignored = 0
        known_paths = {str(Path(path).resolve()).casefold() for path in self.pdf_paths}
        for filename in filenames:
            path = Path(filename)
            if path.suffix.lower() != ".pdf" or not path.is_file():
                ignored += 1
                continue
            normalized = str(path.resolve())
            if normalized.casefold() in known_paths:
                continue
            self.pdf_paths.append(normalized)
            self.file_list.insert(tk.END, path.name)
            known_paths.add(normalized.casefold())
            added += 1
        self.files_label.configure(text=f"PDF sélectionnés ({len(self.pdf_paths)})")
        if added or ignored:
            message = f"{added} PDF ajouté(s)."
            if ignored:
                message += f" {ignored} élément(s) ignoré(s) : seuls les PDF sont acceptés."
            self.status.set(message)
        elif self.pdf_paths:
            self.status.set(f"{len(self.pdf_paths)} fichier(s) prêt(s) à traiter.")

    def clear_pdfs(self):
        self.pdf_paths.clear()
        self.file_list.delete(0, tk.END)
        self.files_label.configure(text="PDF sélectionnés (0)")

        self.status.set("Ajoutez un ou plusieurs fichiers PDF.")

    def remove_selected_pdfs(self, _event=None):
        selected = list(self.file_list.curselection())
        if not selected:
            return "break"
        for index in reversed(selected):
            self.file_list.delete(index)
            del self.pdf_paths[index]
        self.files_label.configure(text=f"PDF sélectionnés ({len(self.pdf_paths)})")
        self.status.set(f"{len(selected)} fichier(s) retiré(s) de la liste.")
        return "break"

    def choose_output_folder(self):
        initial = self.output_folder.get()
        if not initial and self.pdf_paths:
            initial = str(Path(self.pdf_paths[0]).parent)
        selected = filedialog.askdirectory(
            title="Choisir le dossier de destination",
            initialdir=initial or None,
            mustexist=True,
        )
        if selected:
            self.output_folder.set(selected)

    @staticmethod
    def _next_output_path(folder, source):
        source_path = Path(source)
        base = folder / f"{source_path.stem}_filigrane"
        candidate = base.with_suffix(".pdf")
        number = 2
        while candidate.exists():
            candidate = folder / f"{base.name}_{number}.pdf"
            number += 1
        return candidate

    @staticmethod
    def _stamp_page(page, text, font_size, angle):
        bounds = page.rect
        text_width = fitz.get_text_length(text, fontname="helv", fontsize=font_size)
        step_x = max(text_width + font_size * 2.4, font_size * 5)
        step_y = max(font_size * 3.6, 90)
        rotation = fitz.Matrix(1, 1).prerotate(-angle)

        y = -font_size
        row = 0
        while y < bounds.height + font_size:
            x = -text_width - (step_x / 2 if row % 2 else 0)
            while x < bounds.width + text_width:
                origin = fitz.Point(x, y)
                page.insert_text(
                    origin,
                    text,
                    fontname="helv",
                    fontsize=font_size,
                    color=(0.76, 0.79, 0.85),
                    morph=(origin, rotation),
                    overlay=True,
                )
                x += step_x
            y += step_y
            row += 1

    def export_pdfs(self):
        if fitz is None:
            messagebox.showerror(
                "Bibliothèque manquante",
                "PyMuPDF n'est pas installé dans l'interpréteur Python de ce projet.",
            )
            return
        if not self.pdf_paths:
            messagebox.showwarning("PDF requis", "Ajoutez au moins un fichier PDF.")
            return

        text = self.watermark.get().strip()
        if not text:
            messagebox.showwarning("Texte requis", "Saisissez le texte du filigrane.")
            self.watermark_entry.focus_set()
            return

        try:
            font_size = int(self.font_size.get())
            angle = int(self.rotation.get())
        except (ValueError, tk.TclError):
            messagebox.showwarning("Réglages invalides", "Vérifiez la taille et l'inclinaison.")
            return

        output_text = self.output_folder.get().strip()
        output_folder = Path(output_text) if output_text else Path(self.pdf_paths[0]).parent
        output_folder.mkdir(parents=True, exist_ok=True)

        completed = []
        errors = []
        for source in self.pdf_paths:
            destination = self._next_output_path(output_folder, source)
            try:
                with fitz.open(source) as document:
                    if document.is_encrypted:
                        raise ValueError("PDF protégé par un mot de passe")
                    for page in document:
                        self._stamp_page(page, text, font_size, angle)
                    document.save(str(destination), garbage=4, deflate=True)
                completed.append(destination.name)
            except Exception as error:
                errors.append(f"{Path(source).name} : {error}")

        self.status.set(f"Terminé : {len(completed)} PDF créé(s), {len(errors)} erreur(s).")
        summary = f"{len(completed)} PDF filigrané(s) enregistré(s) dans :\n{output_folder}"
        if completed:
            summary += "\n\n" + "\n".join(completed)
        if errors:
            summary += "\n\nFichiers non traités :\n" + "\n".join(errors)
            messagebox.showwarning("Traitement terminé avec des erreurs", summary)
        else:
            messagebox.showinfo("Traitement terminé", summary)


if __name__ == "__main__":
    root = TkinterDnD.Tk() if TkinterDnD is not None else tk.Tk()
    FiligranePDF(root)
    root.mainloop()
