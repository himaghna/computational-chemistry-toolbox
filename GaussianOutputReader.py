import tkinter as tk
import tkinter.ttk as ttk
import os
import read_gaussian_logfile_electronic as readelectronic
import read_gaussian_phosphine_structure as readphosphine
from helper_functions import get_phosphine_carbon_numbers as getphosC
from helper_functions import truncate_to_mulliken, truncate_to_APT, truncate_pre_optimized

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
                outfile.write("filename ")
                if doBL: outfile.write("C1-P Bond Length\tC2-P Bond Length\tC3-P Bond Length\t")
                if doBA: outfile.write("C1-P-C2 Bond Angle\tC1-P-C3 Bond Angle\tC2-P-C3 Bond Angle\t")
                if doMUL: outfile.write("P Mulliken Charge\tC1 Mulliken Charge\tC2 Mulliken Charge C3\tMulliken Charge\t")
                if doAPT: outfile.write("P APT Charge\tC1 APT Charge\tC2 APT Charge\tC3 APT Charge\t")
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
                        # arguments for each finding functions
                        path = input_directory.get() + filename
                        try:
                            truncpath = truncate_pre_optimized(path)
                        except FileNotFoundError:
                            outfile.writelines("Unable to parse!")
                            continue
                        Catoms = getphosC(path)

                        # write each column
                        if doBL: 
                            temp = readphosphine.get_C_P_bond_lengths(truncpath,Catoms)
                            temp = "\t".join([str(i) for i in temp])
                            outfile.write((temp if not isinstance(temp,bool) else "not found")+"\t")

                        if doBA: 
                            temp = readphosphine.get_C_P_C_bond_angles(truncpath,Catoms)
                            temp = "\t".join([str(i) for i in temp])
                            outfile.write((temp if not isinstance(temp,bool) else "not found")+"\t")

                        tempMUL = truncate_to_mulliken(truncpath)
                        if doMUL: 
                            temp = readphosphine.get_mulliken_charges(tempMUL,Catoms)
                            temp = "\t".join([str(i) for i in temp])
                            outfile.write((temp if not isinstance(temp,bool) else "not found")+"\t")

                        tempAPT = truncate_to_APT(tempMUL)
                        if doAPT: 
                            temp = readphosphine.get_APT_charges(tempAPT,Catoms)
                            temp = "\t".join([str(i) for i in temp])
                            outfile.write((temp if not isinstance(temp,bool) else "not found")+"\t")

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

