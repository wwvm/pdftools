import tkinter as tk
from tkinter.filedialog import askopenfilename
import PyPDF2


class PdfToolkit:
    def layout(self):
        self.root = tk.Tk()
        self.root.title = "PDF replace"
        self.path = tk.Text(self.root)
        self.path.grid(row=1,column=0,columnspan=4)
        tk.Button(self.root, text='Source', command=lambda:self.choose(0)).grid(row=0,column=0)
        tk.Button(self.root, text='Target', command=lambda:self.choose(1)).grid(row=0,column=1)
        self.page = tk.Entry(self.root, text='page')
        self.page.grid(row=0,column=2)
        tk.Button(self.root, text='Replace', command=self.replace).grid(row=0,column=3)
        return self.root

    def replace(self):
        import PyPDF2 as pdf
        try:
            src = pdf.PdfFileReader(self.source)
            src2 = pdf.PdfFileReader(self.target)
            total = src.getNumPages()
            if self.page.get() == '':
                page = total
            else:
                page = int(self.page.get())
                if page <= 0 or page >= total:
                    page = total;
            writer = pdf.PdfFileWriter()
            for p in range(page - 1):
                writer.addPage(src.getPage(p))
            writer.addPage(src2.getPage(0))
            for p in range(page, total):
                writer.addPage(src.getPage(p))

            dstFile = 'replaced.pdf'
            fo = open(dstFile, 'wb+')
            writer.write(fo)
            fo.close()
            self.path.insert(tk.END, 'Replace finished\n')
        except Exception as s:
            self.path.insert(tk.END, s)
            self.path.insert(tk.END, '\n')

    def choose(self, var):
        filename = askopenfilename(parent=self.root, filetypes=[('Pdf Files', '*.pdf')], title='Select a pdf file')
        self.path.insert(tk.END, filename + '\n')
        if var == 0:
            self.source = filename
        else:
            self.target = filename


if __name__ == '__main__':
    PdfToolkit().layout().mainloop()

