import tkinter as tk
import tkinter.ttk as ttk
from enigma_machine import EnigmaMachine

# This is a tkinter-based GUI for Enigma Machine.


class MainApp(tk.Frame, EnigmaMachine):
    """this is Enigma Machine GUI
    """

    def __init__(self, *args, **kwargs):
        """init main window

        Attributes:
            button_list (list): list of commutator (plugboard) buttons 
                that will remain in a commutator window
            button_list_updated (list): list of updated commutator 
                buttons that will be added to the rest in the window.
            style = instance of ttk.Style() 

        """
        tk.Frame.__init__(self, *args, **kwargs)
        EnigmaMachine.__init__(self, *args, **kwargs)
        self.initUI()
        self.button_list = []
        self.button_list_updated = []
        self.style = ttk.Style()

    def initUI(self):
        """
        Building the parent window

        Sections:
            MainFrame: all configs related to the parent window
            Translator board: top part of the frame where input-output 
                windows are
            Direct IO: part related to unencrypted text IO
            Encrypted IO: part related to encrypted text IO
            Buttonboard: middle section between Direct IO and 
                Encrypted IO, contains encrypt-decrypt buttons
            Baseboard: bottom portion of the window, that contains 
                'reset', 'comm settings' buttons, rotor set
                and rotor position controls.
            Commutator: commutator button
            Reset: reset button
            Rotor Position Wheels: three windows allowing to set up rotor
                positions
            Rotors Selected: dropdown menu allowing to pick certain rotor
                numbers
        """
        self.master.geometry('800x500')  # size of the window upon opening
        self.master.title('Enigma Machine v1.0')
        self.master.minsize(750, 200)
        self.master.grid_propagate(
            'False')  # Slaves do not determine the size of the master widget
        self.pack(fill='both', expand=True)

        # MainFrame
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill='both', expand=1)

        self.mainFrame.rowconfigure(0, weight=3)
        self.mainFrame.columnconfigure(0, weight=1)

        # Translator board
        self.translator_board = tk.Frame(self.mainFrame)
        self.translator_board.grid(column=0, row=0, sticky='nsew')

        self.translator_board.columnconfigure(0, weight=1)
        self.translator_board.rowconfigure(2, weight=1)
        self.translator_board.columnconfigure(2, weight=1)

        # Direct IO
        self.direct_label = tk.LabelFrame(self.translator_board,
                                          text='Direct',
                                          padx=5,
                                          pady=5)
        self.direct_label.grid(column=0,
                               row=0,
                               rowspan=3,
                               padx=5,
                               pady=5,
                               sticky='nsew')

        self.direct_label.rowconfigure(0, weight=1)
        self.direct_label.columnconfigure(0, weight=1)

        self.direct_input = tk.Text(self.direct_label)
        self.direct_input.grid(column=0, row=0, sticky='nsew', padx=0, pady=0)
        direct_scroller = ttk.Scrollbar(self.direct_label,
                                        command=self.direct_input.yview)
        direct_scroller.grid(column=1, row=0, sticky='NSE')
        self.direct_input['yscrollcommand'] = direct_scroller.set

        # Encrypted IO
        self.encrypted_label = tk.LabelFrame(self.translator_board,
                                             text='Encrypted',
                                             padx=5,
                                             pady=5)
        self.encrypted_label.grid(column=2,
                                  row=0,
                                  rowspan=3,
                                  padx=5,
                                  pady=5,
                                  sticky='nsew')

        self.encrypted_label.rowconfigure(0, weight=1)
        self.encrypted_label.columnconfigure(0, weight=1)

        self.encrypted_input = tk.Text(self.encrypted_label)
        self.encrypted_input.grid(column=0,
                                  row=0,
                                  padx=0,
                                  pady=0,
                                  sticky='nsew')
        encrypted_scroller = ttk.Scrollbar(self.encrypted_label,
                                           command=self.encrypted_input.yview)
        encrypted_scroller.grid(column=1, row=0, sticky='NSE')
        self.encrypted_input['yscrollcommand'] = encrypted_scroller.set

        # ButtonBoard
        button_board = tk.Frame(self.translator_board, width=80, height=100)
        button_board.grid(column=1, row=2)

        self.encode = ttk.Button(button_board, text='>>>')
        self.encode.config(command=lambda: self.onEncode())
        self.encode.place(relx=0.5, rely=0.30, anchor='center')

        self.decode = ttk.Button(button_board, text='<<<')
        self.decode.config(command=lambda: self.onDecode())
        self.decode.place(relx=0.5, rely=0.70, anchor='center')

        # Baseboard
        baseboard = tk.Frame(self.mainFrame, height=50, pady=5, padx=5)
        baseboard.grid(column=0, row=1, sticky='ew')

        baseboard.columnconfigure(0, weight=1)
        baseboard.columnconfigure(1, weight=1)
        baseboard.columnconfigure(2, weight=1)
        baseboard.rowconfigure(0, weight=1)

        left_button_box = tk.Frame(baseboard)
        left_button_box.grid(column=0, row=0, sticky='W')

        # Commutator button
        self.comm_button = ttk.Button(left_button_box,
                                      text='Open commutator settings')
        self.comm_button.config(command=lambda: self.openCommSettings())
        self.comm_button.grid(column=1, row=0, sticky='e')

        # Reset button
        self.reset_button = ttk.Button(left_button_box, text='Reset')
        self.reset_button.config(command=lambda: self.onReset())
        self.reset_button.grid(column=0, row=0, sticky='w')

        # Mode selector
        self.mode_selector_frame = tk.LabelFrame(
            baseboard, height=50, width=50, text='Mode', padx=5, pady=5)
        self.mode_selector_frame.grid(column=2, row=0, sticky='w')
        self.mode_selector = ttk.Entry(self.mode_selector_frame, width=2)
        self.mode_selector.pack(fill='both')

        self.mode_selector.insert(0, self.mode)

        # Rotor Position Wheels
        positioning_frame = tk.LabelFrame(baseboard,
                                          height=50,
                                          width=250,
                                          text='Current Rotor Position')
        positioning_frame.grid(column=3, row=0, sticky='e')

        self.var1 = tk.IntVar()

        self.position_1 = ttk.Spinbox(positioning_frame,
                                      textvariable=self.var1,
                                      from_=0,
                                      to=25,
                                      width=3,
                                      command=self.setWheels)
        self.position_1.set(self.wheel1pos)
        self.position_1.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)

        self.position_2 = ttk.Spinbox(positioning_frame,
                                      from_=0,
                                      to=25,
                                      width=3,
                                      command=self.setWheels)
        self.position_2.set(self.wheel2pos)
        self.position_2.grid(column=1, row=0, sticky='nsew', padx=5, pady=5)

        self.position_3 = ttk.Spinbox(positioning_frame,
                                      from_=0,
                                      to=25,
                                      width=3,
                                      command=self.setWheels)
        self.position_3.set(self.wheel3pos)
        self.position_3.grid(column=2, row=0, sticky='nsew', padx=5, pady=5)

        # Rotors Selected
        rotors_frame = tk.LabelFrame(baseboard,
                                     text='Rotors',
                                     width=250,
                                     padx=5)
        rotors_frame.grid(column=2, row=0, sticky='E', padx=5)

        rotor_options = list(self.rotors)

        self.rotor1_value = tk.IntVar(self)
        self.rotor2_value = tk.IntVar(self)
        self.rotor3_value = tk.IntVar(self)

        rotor1_label = ttk.Label(rotors_frame, text='1:')
        rotor1_label.grid(column=0, row=0, sticky='E')
        self.rotor1 = ttk.OptionMenu(rotors_frame, self.rotor1_value,
                                     rotor_options[0], *rotor_options)
        self.rotor1.grid(row=0, column=1, padx=5, pady=2, sticky='W')

        rotor2_label = ttk.Label(rotors_frame, text='2:')
        rotor2_label.grid(column=2, row=0, sticky='E')
        self.rotor2 = ttk.OptionMenu(rotors_frame, self.rotor2_value,
                                     rotor_options[0], *rotor_options)
        self.rotor2.grid(row=0, column=3, padx=5, pady=2, sticky='W')

        rotor3_label = ttk.Label(rotors_frame, text='3:')
        rotor3_label.grid(column=4, row=0, sticky='E')
        self.rotor3 = ttk.OptionMenu(rotors_frame, self.rotor3_value,
                                     rotor_options[0], *rotor_options)
        self.rotor3.grid(row=0, column=5, padx=5, pady=2, sticky='W')

    def onEncode(self):
        self.setWheels()
        self.mode = int(self.mode_selector.get())
        direct = self.direct_input.get("1.0", tk.END)
        self.encrypted_input.delete("1.0", tk.END)
        self.encrypted_input.insert("1.0", self.encrypt(direct))

        self.wheelClick()

    def onDecode(self):
        self.setWheels()
        encrypted = self.encrypted_input.get("1.0", tk.END)
        self.direct_input.delete("1.0", tk.END)
        self.direct_input.insert("1.0", self.decrypt(encrypted))
        self.wheelClick()

    def onReset(self):
        self.direct_input.delete("1.0", tk.END)
        self.encrypted_input.delete("1.0", tk.END)
        self.positionSetter([0, 0, 0])
        self.wheelClick()

    def setWheels(self):
        self.rotor_set = str(self.rotor1_value.get()) + str(
            self.rotor2_value.get()) + str(self.rotor3_value.get())
        self.positionSetter([
            int(self.position_1.get()),
            int(self.position_2.get()),
            int(self.position_3.get())
        ])

    def wheelClick(self):
        self.position_1.set(self.wheel1pos)
        self.position_2.set(self.wheel2pos)
        self.position_3.set(self.wheel3pos)

    def openCommSettings(self):
        """
        This is child window that opens after 'Comm Settings' 
        button press

        """
        # Window settings
        self.comm_window = tk.Toplevel(self.master)
        self.comm_window.geometry('230x215')
        self.comm_window.title('Commutator Settings')
        self.comm_window.grab_set()
        self.comm_window.bind('<Return>', lambda event: self.on_add_link())

        # grid layout
        self.comm_window.columnconfigure(0, weight=1)
        self.comm_window.columnconfigure(1, weight=1)

        # control frame: entry + add_button
        self.control_frame = tk.Frame(self.comm_window, height=30)
        self.control_frame.grid(row=0, columnspan=2, column=0, sticky='nsew')

        self.couple_var = tk.StringVar()
        self.couple_entry = tk.Entry(
            self.control_frame, width=4, textvariable=self.couple_var
        )
        self.couple_entry.pack(side='left', pady=10, padx=10)

        self.add_button = ttk.Button(self.control_frame, text='Add link')
        self.add_button.config(command=lambda: self.on_add_link())
        self.add_button.pack(side='left', pady=5, padx=10,
                             fill='both', expand=1)

        self.button_creator(
        )  # init exising links as buttons when the comm_board is open:

    # ADDS COUPLE AND BUTTON
    def on_add_link(self):
        # Checking the input before adding it:
        if self.couple_entry.get().upper().isalpha() and len(self.couple_entry.get().upper()) == 2: ##ENG
            # adding pair to the self.plugboard
            self.add_pair(self.couple_entry.get().upper())
            # creating entry for the button to be initialized
            self.button_list_updated = []
            for pair in self.plugboard:
                self.button_list_updated.append(''.join(list(pair)))
            self.couple_entry.delete(0, tk.END)
            # callback creator
            self.button_creator()
        else:
            self.couple_entry.delete(0, tk.END)

    # DELETION

    def on_linkbutton_click(self, letters):
        for letter in letters:
            self.unpair_letter(letter)
        # callback creator
        self.button_creator()

    # CREATES BUTTONS ON THE FORM
    def button_creator(self):
        # Deleting all existing buttons,
        # to check if there any that are deleted:
        for widget in self.comm_window.winfo_children()[1:]:
            widget.destroy()

        # Creating buttons in accordance with self.plugboard:
        counter = 0
        for pair in self.plugboard:
            counter += 1
            couple = ''.join(list(pair))
            self.button_link = ttk.Button(
                self.comm_window,
                text=f'{couple}',
                command=lambda x=couple: self.on_linkbutton_click(x))  # deletion function is bound to a text variable of a button.
            if len(self.plugboard) < 7:
                # buttons occupy the whole window
                self.button_link.grid(
                    row=counter+1, columnspan=2, column=0, sticky='nsew')
            else:
                # buttons occupy half and half
                if counter < 7:
                    self.button_link.grid(
                        row=counter+1, column=0, sticky='nsew')
                else:
                    self.button_link.grid(
                        row=counter-5, column=1, sticky='nsew')

    # THIS SECTION WAS USED FOR A DIFFERENT UI STYLE

    #     #Init CommUI
    #     self.comm_window = tk.Toplevel(self.master)
    #     self.comm_window.geometry('430x215')
    #     self.comm_window.resizable(False, False)
    #     self.comm_window.title('Commutator Settings')
    #     self.comm_window.grab_set()

    #     for i in range(14):
    #         self.comm_window.columnconfigure(i, weight=1)

    #     for j in range(6):
    #         self.comm_window.rowconfigure(j, weight=1)

    #     #A
    #     self.a_var = tk.StringVar()
    #     # self.a_var.set(self.plugboard[0])
    #     a_label = tk.Label(self.comm_window, text='A→')
    #     a_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='')
    #     self.a_entry = tk.Entry(self.comm_window, width=2, textvariable=self.a_var)
    #     self.a_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky='EW')

    #     #B
    #     self.b_var = tk.StringVar()
    #     # b_var.set(self.plugboard[1])
    #     b_label = tk.Label(self.comm_window, text='B→')
    #     b_label.grid(row=1, column=2, padx=(10, 0), pady=10, sticky='')
    #     self.b_entry = tk.Entry(self.comm_window, width=2, textvariable=self.b_var)
    #     self.b_entry.grid(row=1, column=3, padx=(0, 10), pady=10, sticky='EW')

    #     #C
    #     self.c_var = tk.StringVar()
    #     #self.c_var.set(self.plugboard[2])
    #     c_label = tk.Label(self.comm_window, text='C→')
    #     c_label.grid(row=1, column=4, padx=(10, 0), pady=10, sticky='')
    #     self.c_entry = tk.Entry(self.comm_window, width=2, textvariable=self.c_var)
    #     self.c_entry.grid(row=1, column=5, padx=(0, 10), pady=10, sticky='EW')

    #     #D
    #     self.d_var = tk.StringVar()
    #     #self.d_var.set(self.plugboard[3])
    #     d_label = tk.Label(self.comm_window, text='D→')
    #     d_label.grid(row=1, column=6, padx=(10, 0), pady=10, sticky='')
    #     self.d_entry = tk.Entry(self.comm_window, width=2, textvariable=self.d_var)
    #     self.d_entry.grid(row=1, column=7, padx=(0, 10), pady=10, sticky='EW')

    #     #E
    #     self.e_var = tk.StringVar()
    #     #self.e_var.set(self.plugboard[4])
    #     e_label = tk.Label(self.comm_window, text='E→')
    #     e_label.grid(row=1, column=8, padx=(10, 0), pady=10, sticky='')
    #     self.e_entry = tk.Entry(self.comm_window, width=2, textvariable=self.e_var)
    #     self.e_entry.grid(row=1, column=9, padx=(0, 10), pady=10, sticky='EW')

    #     #F
    #     self.f_var = tk.StringVar()
    #     #self.f_var.set(self.plugboard[5])
    #     f_label = tk.Label(self.comm_window, text='F→')
    #     f_label.grid(row=1, column=10, padx=(10, 0), pady=10, sticky='')
    #     self.f_entry = tk.Entry(self.comm_window, width=2, textvariable=self.f_var)
    #     self.f_entry.grid(row=1, column=11, padx=(0, 10), pady=10, sticky='EW')

    #     #G
    #     self.g_var = tk.StringVar()
    #     #self.g_var.set(self.plugboard[6])
    #     g_label = tk.Label(self.comm_window, text='G→')
    #     g_label.grid(row=1, column=12, padx=(10, 0), pady=10, sticky='')
    #     self.g_entry = tk.Entry(self.comm_window, width=2, textvariable=self.g_var)
    #     self.g_entry.grid(row=1, column=13, padx=(0, 10), pady=10, sticky='EW')

    #     #H
    #     self.h_var = tk.StringVar()
    #     #self.h_var.set(self.plugboard[7])
    #     h_label = tk.Label(self.comm_window, text='H→')
    #     h_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='')
    #     self.h_entry = tk.Entry(self.comm_window, width=2, textvariable=self.h_var)
    #     self.h_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky='EW')

    #     #I
    #     self.i_var = tk.StringVar()
    #     #self.i_var.set(self.plugboard[8])
    #     i_label = tk.Label(self.comm_window, text='I→')
    #     i_label.grid(row=2, column=2, padx=(10, 0), pady=10, sticky='')
    #     self.i_entry = tk.Entry(self.comm_window, width=2, textvariable=self.i_var)
    #     self.i_entry.grid(row=2, column=3, padx=(0, 10), pady=10, sticky='EW')

    #     #J
    #     self.j_var = tk.StringVar()
    #     #self.j_var.set(self.plugboard[9])
    #     j_label = tk.Label(self.comm_window, text='J→')
    #     j_label.grid(row=2, column=4, padx=(10, 0), pady=10, sticky='')
    #     self.j_entry = tk.Entry(self.comm_window, width=2, textvariable=self.j_var)
    #     self.j_entry.grid(row=2, column=5, padx=(0, 10), pady=10, sticky='EW')

    #     #K
    #     self.k_var = tk.StringVar()
    #     #self.k_var.set(self.plugboard[10])
    #     k_label = tk.Label(self.comm_window, text='K→')
    #     k_label.grid(row=2, column=6, padx=(10, 0), pady=10, sticky='')
    #     self.k_entry = tk.Entry(self.comm_window, width=2, textvariable=self.k_var)
    #     self.k_entry.grid(row=2, column=7, padx=(0, 10), pady=10, sticky='EW')

    #     #L
    #     self.l_var = tk.StringVar()
    #     #self.l_var.set(self.plugboard[11])
    #     l_label = tk.Label(self.comm_window, text='L→')
    #     l_label.grid(row=2, column=8, padx=(10, 0), pady=10, sticky='')
    #     self.l_entry = tk.Entry(self.comm_window, width=2, textvariable=self.l_var)
    #     self.l_entry.grid(row=2, column=9, padx=(0, 10), pady=10, sticky='EW')

    #     #M
    #     self.m_var = tk.StringVar()
    #     #self.m_var.set(self.plugboard[12])
    #     m_label = tk.Label(self.comm_window, text='M→')
    #     m_label.grid(row=2, column=10, padx=(10, 0), pady=10, sticky='')
    #     self.m_entry = tk.Entry(self.comm_window, width=2, textvariable=self.m_var)
    #     self.m_entry.grid(row=2, column=11, padx=(0, 10), pady=10, sticky='EW')

    #     #N
    #     self.n_var = tk.StringVar()
    #     #self.n_var.set(self.plugboard[13])
    #     n_label = tk.Label(self.comm_window, text='N→')
    #     n_label.grid(row=2, column=12, padx=(10, 0), pady=10, sticky='')
    #     self.n_entry = tk.Entry(self.comm_window, width=2, textvariable=self.n_var)
    #     self.n_entry.grid(row=2, column=13, padx=(0, 10), pady=10, sticky='EW')

    #     #O
    #     self.o_var = tk.StringVar()
    #     #self.o_var.set(self.plugboard[14])
    #     o_label = tk.Label(self.comm_window, text='O→')
    #     o_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky='')
    #     self.o_entry = tk.Entry(self.comm_window, width=2, textvariable=self.o_var)
    #     self.o_entry.grid(row=3, column=1, padx=(0, 10), pady=10, sticky='EW')

    #     #P
    #     self.p_var = tk.StringVar()
    #     #self.p_var.set(self.plugboard[15])
    #     p_label = tk.Label(self.comm_window, text='P→')
    #     p_label.grid(row=3, column=2, padx=(10, 0), pady=10, sticky='')
    #     self.p_entry = tk.Entry(self.comm_window, width=2, textvariable=self.p_var)
    #     self.p_entry.grid(row=3, column=3, padx=(0, 10), pady=10, sticky='EW')

    #     #Q
    #     self.q_var = tk.StringVar()
    #     #self.q_var.set(self.plugboard[16])
    #     q_label = tk.Label(self.comm_window, text='Q→')
    #     q_label.grid(row=3, column=4, padx=(10, 0), pady=10, sticky='')
    #     self.q_entry = tk.Entry(self.comm_window, width=2, textvariable=self.q_var)
    #     self.q_entry.grid(row=3, column=5, padx=(0, 10), pady=10, sticky='EW')

    #     #R
    #     self.r_var = tk.StringVar()
    #     #self.r_var.set(self.plugboard[17])
    #     r_label = tk.Label(self.comm_window, text='R→')
    #     r_label.grid(row=3, column=6, padx=(10, 0), pady=10, sticky='')
    #     self.r_entry = tk.Entry(self.comm_window, width=2, textvariable=self.r_var)
    #     self.r_entry.grid(row=3, column=7, padx=(0, 10), pady=10, sticky='EW')

    #     #S
    #     self.s_var = tk.StringVar()
    #     #self.s_var.set(self.plugboard[18])
    #     s_label = tk.Label(self.comm_window, text='S→')
    #     s_label.grid(row=3, column=8, padx=(10, 0), pady=10, sticky='')
    #     self.s_entry = tk.Entry(self.comm_window, width=2, textvariable=self.s_var)
    #     self.s_entry.grid(row=3, column=9, padx=(0, 10), pady=10, sticky='EW')

    #     #T
    #     self.t_var = tk.StringVar()
    #     #self.t_var.set(self.plugboard[19])
    #     t_label = tk.Label(self.comm_window, text='T→')
    #     t_label.grid(row=3, column=10, padx=(10, 0), pady=10, sticky='')
    #     self.t_entry = tk.Entry(self.comm_window, width=2, textvariable=self.t_var)
    #     self.t_entry.grid(row=3, column=11, padx=(0, 10), pady=10, sticky='EW')

    #     #U
    #     self.u_var = tk.StringVar()
    #     #self.u_var.set(self.plugboard[20])
    #     u_label = tk.Label(self.comm_window, text='U→')
    #     u_label.grid(row=3, column=12, padx=(10, 0), pady=10, sticky='')
    #     self.u_entry = tk.Entry(self.comm_window, width=2, textvariable=self.u_var)
    #     self.u_entry.grid(row=3, column=13, padx=(0, 10), pady=10, sticky='EW')

    #     #V
    #     self.v_var = tk.StringVar()
    #     #self.v_var.set(self.plugboard[21])
    #     v_label = tk.Label(self.comm_window, text='V→')
    #     v_label.grid(row=4, column=2, padx=(10, 0), pady=10, sticky='')
    #     self.v_entry = tk.Entry(self.comm_window, width=2, textvariable=self.v_var)
    #     self.v_entry.grid(row=4, column=3, padx=(0, 10), pady=10, sticky='EW')

    #     #W
    #     self.w_var = tk.StringVar()
    #     #self.w_var.set(self.plugboard[22])
    #     w_label = tk.Label(self.comm_window, text='W→')
    #     w_label.grid(row=4, column=4, padx=(10, 0), pady=10, sticky='')
    #     self.w_entry = tk.Entry(self.comm_window, width=2, textvariable=self.w_var)
    #     self.w_entry.grid(row=4, column=5, padx=(0, 10), pady=10, sticky='EW')

    #     #X
    #     self.x_var = tk.StringVar()
    #     #self.x_var.set(self.plugboard[23])
    #     x_label = tk.Label(self.comm_window, text='X→')
    #     x_label.grid(row=4, column=6, padx=(10, 0), pady=10, sticky='')
    #     self.x_entry = tk.Entry(self.comm_window, width=2, textvariable=self.x_var)
    #     self.x_entry.grid(row=4, column=7, padx=(0, 10), pady=10, sticky='EW')

    #     #Y
    #     self.y_var = tk.StringVar()
    #     #self.y_var.set(self.plugboard[24])
    #     y_label = tk.Label(self.comm_window, text='Y→')
    #     y_label.grid(row=4, column=8, padx=(10, 0), pady=10, sticky='')
    #     self.y_entry = tk.Entry(self.comm_window, width=2, textvariable=self.y_var)
    #     self.y_entry.grid(row=4, column=9, padx=(0, 10), pady=10, sticky='EW')

    #     #Z
    #     self.z_var = tk.StringVar()
    #     #self.z_var.set(self.plugboard[25])
    #     z_label = tk.Label(self.comm_window, text='Z→')
    #     z_label.grid(row=4, column=10, padx=(10, 0), pady=10, sticky='')
    #     self.z_entry = tk.Entry(self.comm_window, width=2, textvariable=self.z_var)
    #     self.z_entry.grid(row=4, column=11, padx=(0, 10), pady=10, sticky='EW')

    #     #Save button
    #     self.comm_save = ttk.Button(self.comm_window, text='Save')
    #     self.comm_save.config(command=lambda: self.on_comm_save())
    #     self.comm_save.grid(row=5, column=6, columnspan=2, pady=10)

    # def on_comm_save(self):
    #     entry_list = [
    #         self.a_entry,
    #         self.b_entry,
    #         self.c_entry,
    #         self.d_entry,
    #         self.e_entry,
    #         self.f_entry,
    #         self.g_entry,
    #         self.h_entry,
    #         self.i_entry,
    #         self.j_entry,
    #         self.k_entry,
    #         self.l_entry,
    #         self.m_entry,
    #         self.n_entry,
    #         self.o_entry,
    #         self.p_entry,
    #         self.q_entry,
    #         self.r_entry,
    #         self.s_entry,
    #         self.t_entry,
    #         self.u_entry,
    #         self.v_entry,
    #         self.w_entry,
    #         self.x_entry,
    #         self.y_entry,
    #         self.z_entry
    #     ]

    #     output_list = [self.a_var,
    #                    self.b_var,
    #                    self.c_var,
    #                    self.d_var,
    #                    self.e_var,
    #                     self.f_var,
    #                     self.g_var,
    #                     self.h_var,
    #                     self.i_var,
    #                     self.j_var,
    #                     self.k_var,
    #                     self.l_var,
    #                     self.m_var,
    #                     self.n_var,
    #                     self.o_var,
    #                     self.p_var,
    #                     self.q_var,
    #                     self.r_var,
    #                     self.s_var,
    #                     self.t_var,
    #                     self.u_var,
    #                     self.v_var,
    #                     self.w_var,
    #                     self.x_var,
    #                     self.y_var,
    #                     self.z_var]

    #     # ADDS A LETTER TO A PAIR
    #     # for index, entry in enumerate(entry_list):
    #     #     if entry.get() != '':
    #     #         output_list[ord(entry.get().upper())-65].set(self.direct[index])

    #     # ADDS PAIR TO THE PLUGBOARD
    #     for index, entry in enumerate(entry_list):
    #         letter = self.direct[index]
    #         if entry.get() in list(string.ascii_letters) and entry.get() != letter:
    #             self.add_pair(letter+entry.get().upper())
    #         # elif entry.get() not in list(string.ascii_letters):
    #         #     self.unpair_letter(letter)

    #         # self.plugboard = self.plugboard[:index] + entry.get().upper() + self.plugboard[index+1:] # Entered letter gets recorded into plugboard

    #         # # IF other letter is unpaired:
    #         # if self.plugboard[(ord(entry.get().upper()) - 65)] == self.direct[(ord(entry.get().upper()) - 65)]:
    #         #     self.plugboard = self.plugboard[:(ord(entry.get().upper()) - 65)] + letter + self.plugboard[(ord(entry.get().upper()) - 65)+1:]

    #         # # If other letter is already in pair with a different letter:
    #         # elif self.plugboard[(ord(entry.get().upper()) - 65)] != entry.get().upper():
    #         #     self.plugboard = self.plugboard[:(ord(entry.get().upper()) - 65)] + self.direct[(ord(entry.get().upper()) - 65)] + self.plugboard[(ord(entry.get().upper()) - 65)+1:]
    #         #     self.plugboard = self.plugboard[:(ord(entry.get().upper()) - 65)] + letter + self.plugboard[(ord(entry.get().upper()) - 65)+1:]

    #     # SETS VALUES BASED ON PLUGBOARD CONFIG
    #     for index, value in enumerate(output_list):
    #         for pair in self.plugboard:
    #             if set(self.direct[index]).issubset(pair):
    #                 value.set(list(pair.difference(set(self.direct[index])))[0])
    #                 #output_list[ord(list(pair.difference(set(self.direct[index])))[0])-65].set('4')
    #                 break
    #         else:
    #             value.set('')

    #     print(self.plugboard)


if __name__ == '__main__':
    # Running the app
    root = tk.Tk()
    app = MainApp()
    # app.style.theme_use('winnative')
    root.mainloop()
