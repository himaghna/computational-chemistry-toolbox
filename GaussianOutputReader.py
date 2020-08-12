import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os
from tools.helper_functions import get_phosphine_phosphorus_number as getphosP
from tools.helper_functions import get_phosphine_atom_numbers as getphosAs
from tools.helper_functions import truncate_to_mulliken, truncate_to_APT, truncate_pre_optimized
from tools import read_gaussian_logfile_electronic as readelectronic
from tools import read_gaussian_phosphine_structure as readphosphine


class GaussianOutputReader:
    def __init__(self, master=None):
        # build ui
        main_frame = ttk.Frame(master)
        input_dir_label = ttk.Label(main_frame)
        input_dir_label.config(anchor='w', takefocus=False, text='Directory Containing Gaussian Output Files')
        input_dir_label.pack(side='top')
        input_directory = ttk.Entry(main_frame)
        input_directory.config(exportselection='true', font='TkDefaultFont', state='normal', takefocus=False)
        input_directory.config(validate='none')
        _text_ = '''input directory'''
        input_directory.delete('0', 'end')
        input_directory.insert('0', _text_)
        input_directory.pack(fill='both', side='top')
        output_name_label = ttk.Label(main_frame)
        output_name_label.config(takefocus=False, text='Name for Output File')
        output_name_label.pack(side='top')
        output_name = ttk.Entry(main_frame)
        _text_ = '''output name'''
        output_name.delete('0', 'end')
        output_name.insert('0', _text_)
        output_name.pack(side='top')
        phosphine_properties_label = ttk.Label(main_frame)
        phosphine_properties_label.config(text='Phosphine Properties:')
        phosphine_properties_label.pack(side='top')
        bondlength_button = ttk.Checkbutton(main_frame)
        bondlength_button.config(state='normal', text='C-P Bond Lengths')
        bondlength_button.pack(side='top')
        bond_angle_button = ttk.Checkbutton(main_frame)
        bond_angle_button.config(text='C-P-C Bond Angles')
        bond_angle_button.pack(side='top')
        mulliken_button = ttk.Checkbutton(main_frame)
        mulliken_button.config(compound='bottom', takefocus=True, text='Mulliken Charges')
        mulliken_button.pack(side='top')
        apt_button = ttk.Checkbutton(main_frame)
        apt_button.config(text='APT Charges')
        apt_button.pack(side='top')
        electronic_properties_label = ttk.Label(main_frame)
        electronic_properties_label.config(compound='top', text='Electronic Properties:')
        electronic_properties_label.pack(side='top')
        zpe_button = ttk.Checkbutton(main_frame)
        zpe_button.config(text='ZPE')
        zpe_button.pack(side='top')
        ezpe_button = ttk.Checkbutton(main_frame)
        ezpe_button.config(compound='top', text='Electronic ZPE')
        ezpe_button.pack(side='top')
        freenrg_button = ttk.Checkbutton(main_frame)
        freenrg_button.config(text='Free Energy')
        freenrg_button.pack(side='top')
        enthalpy_button = ttk.Checkbutton(main_frame)
        enthalpy_button.config(cursor='arrow', state='normal', text='Enthalpy')
        enthalpy_button.pack(side='top')

        def get_data():
            doBL = bondlength_button.instate(['selected'])
            doBA = bond_angle_button.instate(['selected'])
            doMUL = mulliken_button.instate(['selected'])
            doAPT = apt_button.instate(['selected'])
            doZPE = zpe_button.instate(['selected'])
            doEZPE = ezpe_button.instate(['selected'])
            doFNRG = freenrg_button.instate(['selected'])
            doENT = enthalpy_button.instate(['selected'])
            with open(
                input_directory.get() + output_name.get() + ".txt", 'w'
            ) as outfile:
                # write header
                outfile.write("filename\t")
                if doBL: outfile.write("A1-P Bond Length\tA2-P Bond Length\tA3-P Bond Length\t")
                if doBA: outfile.write("A1-P-A2 Bond Angle\tA1-P-A3 Bond Angle\tA2-P-A3 Bond Angle\t")
                if doMUL: outfile.write("P Mulliken Charge\tA1 Mulliken Charge\tA2 Mulliken Charge\tA3 Mulliken Charge\t")
                if doAPT: outfile.write("P APT Charge\tA1 APT Charge\tA2 APT Charge\tA3 APT Charge\t")
                if doZPE: outfile.write("ZPE\t")
                if doEZPE: outfile.write("Electronic ZPE\t")
                if doFNRG: outfile.write("Free Energy\t")
                if doENT: outfile.write("enthalpy")
                outfile.write("\n")
                # list all files in the given input directory
                for filename in os.listdir(input_directory.get()):
                    # only search gaussian output files
                    if filename.endswith(".log"):
                        outfile.write(filename+"\t")
                        print("Parsing {}...".format(filename))
                        # arguments for each finding functions
                        path = input_directory.get() + filename
                        try:
                            truncpath = truncate_pre_optimized(path)
                        except FileNotFoundError:
                            outfile.writelines("Unable to parse!")
                            continue
                        Pid = getphosP(path)
                        Cids = getphosAs(path,Pid)

                        # write each column
                        if doBL: 
                            temp = readphosphine.get_A_P_bond_lengths(truncpath,Cids,Pid)
                            # loop through and join with a tab. when False is found, write not found instead
                            outfile.write("\t".join([(str(i) if not isinstance(i,bool) else "not found") for i in temp])+"\t")

                        if doBA: 
                            temp = readphosphine.get_A_P_A_bond_angles(truncpath,Cids,Pid)
                            outfile.write("\t".join([(str(i) if not isinstance(i,bool) else "not found") for i in temp])+"\t")

                        tempMUL = truncate_to_mulliken(truncpath)
                        if doMUL: 
                            temp = readphosphine.get_mulliken_charges(tempMUL,Cids,Pid)
                            outfile.write("\t".join([(str(i) if not isinstance(i,bool) else "not found") for i in temp])+"\t")

                        tempAPT = truncate_to_APT(tempMUL)
                        if doAPT: 
                            temp = readphosphine.get_APT_charges(tempAPT,Cids,Pid)
                            outfile.write("\t".join([(str(i) if not isinstance(i,bool) else "not found") for i in temp])+"\t")

                        if doZPE: 
                            temp = readelectronic.get_zpe(path)
                            outfile.write((str(temp) if not isinstance(temp,bool) else "not found")+"\t")

                        if doEZPE: 
                            temp = readelectronic.get_electronic_zpe(path)
                            outfile.write((str(temp) if not isinstance(temp,bool) else "not found")+"\t")

                        if doFNRG: 
                            temp = readelectronic.get_free_energy(path)
                            outfile.write((str(temp) if not isinstance(temp,bool) else "not found")+"\t")

                        if doENT: 
                            temp = readelectronic.get_enthalpy(path)
                            outfile.write((str(temp) if not isinstance(temp,bool) else "not found"))

                        outfile.write("\n")

                        os.remove(truncpath)
                        os.remove(tempAPT)
                        os.remove(tempMUL)
            if os.path.isfile(input_directory.get() + output_name.get() + ".txt"):
                msg = "Data successfully written to " + input_directory.get() + output_name.get() + ".txt"
                messagebox.showinfo(title="Data Written", message=msg)
            else:
                # likely causes - directory user does not have write access to or directory does not exist
                msg = "Data could not be written! Ensure you have write permission to the input directory and that the directory exists."
                messagebox.showerror(title="Output Error!", message=msg)

        
        go_button = ttk.Button(main_frame)
        go_button.config(compound='bottom', cursor='trek', takefocus=False, text='Go')
        go_button.pack(side='top')
        go_button.configure(command=get_data)
        
        main_frame.config(height='200', takefocus=False, width='200')
        main_frame.pack(side='top')

        # Main widget
        self.mainwindow = main_frame

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk(className='g.o.r.')
    app = GaussianOutputReader(root)
    app.run()

