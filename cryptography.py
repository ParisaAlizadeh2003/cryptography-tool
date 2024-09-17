import wx
import os
import string
import random
from pathlib import Path

encode = ' ' + '\'' + string.ascii_letters + string.digits + string.punctuation
encodelist = list(encode)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title='Cryptography Tool')
        frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 400))
        self.pth = []
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Path selection
        path_panel = wx.Panel(panel)
        path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_path = wx.StaticText(path_panel, label="Path: ")
        path_sizer.Add(lbl_path, 0, wx.ALL | wx.CENTER, 5)
        self.txt_path = wx.TextCtrl(path_panel, size=(300, -1))
        path_sizer.Add(self.txt_path, 1, wx.ALL | wx.EXPAND, 5)
        btn_browse_path = wx.Button(path_panel, label="Browse")
        btn_browse_path.Bind(wx.EVT_BUTTON, self.browse_path)
        path_sizer.Add(btn_browse_path, 0, wx.ALL, 5)
        path_panel.SetSizer(path_sizer)
        main_sizer.Add(path_panel, 0, wx.ALL | wx.EXPAND, 5)

        # Extension selection
        ext_panel = wx.Panel(panel)
        ext_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_extension = wx.StaticText(ext_panel, label="Extension: ")
        ext_sizer.Add(lbl_extension, 0, wx.ALL | wx.CENTER, 5)
        self.txt_extension = wx.TextCtrl(ext_panel, size=(100, -1))
        ext_sizer.Add(self.txt_extension, 1, wx.ALL | wx.EXPAND, 5)
        ext_panel.SetSizer(ext_sizer)
        main_sizer.Add(ext_panel, 0, wx.ALL | wx.EXPAND, 5)

        # Show files button
        btn_show_files = wx.Button(panel, label="Show Files")
        btn_show_files.Bind(wx.EVT_BUTTON, self.show_files)
        main_sizer.Add(btn_show_files, 0, wx.ALL | wx.CENTER, 5)

        # File list
        lbl_files = wx.StaticText(panel, label="Files:")
        main_sizer.Add(lbl_files, 0, wx.ALL, 5)
        self.list_files = wx.ListBox(panel, style=wx.LB_MULTIPLE)
        main_sizer.Add(self.list_files, 1, wx.ALL | wx.EXPAND, 5)

        # Encrypt and decrypt buttons
        btn_encrypt = wx.Button(panel, label="Encrypt")
        btn_encrypt.Bind(wx.EVT_BUTTON, self.encrypt_files)
        main_sizer.Add(btn_encrypt, 0, wx.ALL | wx.CENTER, 5)
        
        btn_decrypt = wx.Button(panel, label="Decrypt")
        btn_decrypt.Bind(wx.EVT_BUTTON, self.decrypt_files)
        main_sizer.Add(btn_decrypt, 0, wx.ALL | wx.CENTER, 5)

        # Secret key path
        secret_panel = wx.Panel(panel)
        secret_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_secret_path = wx.StaticText(secret_panel, label="Secret Key Path: ")
        secret_sizer.Add(lbl_secret_path, 0, wx.ALL | wx.CENTER, 5)
        self.txt_secret = wx.TextCtrl(secret_panel, size=(300, -1))
        secret_sizer.Add(self.txt_secret, 1, wx.ALL | wx.EXPAND, 5)
        btn_browse_secret = wx.Button(secret_panel, label="Browse")
        btn_browse_secret.Bind(wx.EVT_BUTTON, self.browse_secret)
        secret_sizer.Add(btn_browse_secret, 0, wx.ALL, 5)
        secret_panel.SetSizer(secret_sizer)
        main_sizer.Add(secret_panel, 0, wx.ALL | wx.EXPAND, 5)

        # Folder path
        folder_panel = wx.Panel(panel)
        folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_folder_path = wx.StaticText(folder_panel, label="Folder Path: ")
        folder_sizer.Add(lbl_folder_path, 0, wx.ALL | wx.CENTER, 5)
        self.txt_folder_path = wx.TextCtrl(folder_panel, size=(300, -1))
        folder_sizer.Add(self.txt_folder_path, 1, wx.ALL | wx.EXPAND, 5)
        btn_browse_folder = wx.Button(folder_panel, label="Browse")
        btn_browse_folder.Bind(wx.EVT_BUTTON, self.browse_folder)
        folder_sizer.Add(btn_browse_folder, 0, wx.ALL, 5)
        folder_panel.SetSizer(folder_sizer)
        main_sizer.Add(folder_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)
        self.CreateStatusBar()
        self.SetStatusText("Ready")

    def browse_path(self, event):
        with wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.txt_path.SetValue(dlg.GetPath())

    def browse_secret(self, event):
        with wx.FileDialog(self, "Choose the secret key file:", wildcard="Key files (*.key)|*.key",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.txt_secret.SetValue(dlg.GetPath())

    def browse_folder(self, event):
        with wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.txt_folder_path.SetValue(dlg.GetPath())

    def show_files(self, event):
        path = Path(self.txt_path.GetValue())
        extension = self.txt_extension.GetValue()
        if path.exists():
            self.pth.clear()
            self.list_files.Clear()
            for file in path.glob(f'**/*{extension}'):
                self.pth.append(file)
                self.list_files.Append(str(file.relative_to(path)))
        else:
            wx.MessageBox("The specified path does not exist", "Error")

    def encrypt_files(self, event):
        if not self.pth:
            wx.MessageBox("Please specify a valid path and extension", "Error")
            return

        key_list = list(encode)
        random.shuffle(key_list)
        secret_key = ''.join(key_list)

        progress_dialog = wx.ProgressDialog("Encrypting Files",
                                            "Please wait while files are being encrypted...",
                                            maximum=len(self.pth),
                                            parent=self,
                                            style=wx.PD_SMOOTH | wx.PD_AUTO_HIDE)

        try:
            for idx, file_path in enumerate(self.pth):
                with open(file_path, 'rb') as file:
                    content = file.read()
                encrypted_content = bytearray()
                for byte in content:
                    encrypted_content.append(ord(key_list[byte % len(key_list)]))
                with open(file_path, 'wb') as file:
                    file.write(encrypted_content)
                progress_dialog.Update(idx + 1)
            progress_dialog.Destroy()

            with open('secret.key', 'w', encoding='utf-8') as file:
                file.write(secret_key)
            os.startfile('secret.key')
            self.SetStatusText("Encryption completed successfully")

        except Exception as e:
            wx.MessageBox(f"An error occurred: {e}", "Error")
            self.SetStatusText("Encryption failed")
            progress_dialog.Destroy()

    def decrypt_files(self, event):
        try:
            with open(self.txt_secret.GetValue(), 'r', encoding='utf-8') as file:
                secret_key = file.read()
            secret_list = list(secret_key)
        except Exception as e:
            wx.MessageBox(f"An error occurred reading the secret key: {e}", "Error")
            self.SetStatusText("Decryption failed")
            return

        path = Path(self.txt_folder_path.GetValue())
        if not path.exists():
            wx.MessageBox("The specified folder path does not exist", "Error")
            self.SetStatusText("Decryption failed")
            return

        progress_dialog = wx.ProgressDialog("Decrypting Files",
                                            "Please wait while files are being decrypted...",
                                            maximum=len(self.pth),
                                            parent=self,
                                            style=wx.PD_SMOOTH | wx.PD_AUTO_HIDE)

        try:
            for idx, file_path in enumerate(self.pth):
                with open(file_path, 'rb') as file:
                    content = file.read()
                decrypted_content = bytearray()
                for byte in content:
                    decrypted_content.append(encodelist.index(chr(byte)))
                with open(file_path, 'wb') as file:
                    file.write(decrypted_content)
                progress_dialog.Update(idx + 1)
            progress_dialog.Destroy()

            self.SetStatusText("Decryption completed successfully")
        except Exception as e:
            wx.MessageBox(f"An error occurred processing file {file_path}: {e}", "Error")
            self.SetStatusText("Decryption failed")
            progress_dialog.Destroy()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
