
import wx
from views import MainFrame

""" App main file """



class App(wx.App):



	def OnInit(self):

		self.main_frame = MainFrame()
		self.main_frame.Show()

		self.SetTopWindow(self.main_frame)

		return True




if __name__=="__main__":

	app = App()
	app.MainLoop()
