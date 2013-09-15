
import wx
import wx.lib.mixins.listctrl as listmix



# =====================
# Some Custom wxWindows
# =====================


class BackgroundPanel(wx.Panel):


	def __init__(self, parent=None, ID=-1):

		wx.Panel.__init__(self, parent, ID)

		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def OnPaint(self, event):

		dc = wx.BufferedPaintDC(self, self.buffer)


	def OnSize(self, event):

		w, h = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(w, h)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)

		self.Draw(dc)

		self.Refresh()


	def OnEraseBackground(self, event):

		# Vacio intencionalemente
		pass


	def Draw(self, dc):

		w, h = self.GetClientSize()
		dc.Clear()

		bmp = wx.Bitmap("images/wood.png")
		bmp_logo = wx.Bitmap("images/w3bex-logo.png")

		lw, lh = bmp_logo.GetSize()
		bw, bh = bmp.GetSize()

		# Centrar la imagen
		xpos = (w - bw) / 2
		ypos = (h - bh) / 2

		logox = w - lw
		logoy = h - lh

		dc.DrawBitmap(bmp, xpos, ypos)
		dc.DrawBitmap(bmp_logo, logox, logoy)



class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):


	def __init__(self, *args, **kwargs):

		wx.ListCtrl.__init__(self, *args, **kwargs)
		listmix.ListCtrlAutoWidthMixin.__init__(self)



class FormGrid(wx.BoxSizer):


	# Field Data
	KEY = 0
	LABEL = 1
	TYPE = 2
	PROPORTION = 3

	# Field Types
	TEXT_FIELD = 1
	CHOICE_FIELD = 2


	def __init__(self, panel, controls):

		wx.BoxSizer.__init__(self, wx.VERTICAL)

		self.margin = 10
		self.border = 10
		self.panel = panel

		self.controls = {}

		self.setFields(controls)


	def setFields(self, fieldData):

		for line in fieldData:
			sizer = self.createLineSizer(line)
			self.Add(sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)

		self.panel.SetSizer(self)


	def createLineSizer(self, line):

		sizer = wx.BoxSizer(wx.HORIZONTAL)

		for field in line:

			fld = self.createFieldSizer(field)
			sizer.Add(fld, field[self.PROPORTION], wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		return sizer


	def createFieldSizer(self, field):

		label = wx.StaticText(self.panel, label=field[self.LABEL])

		if field[self.TYPE] == self.TEXT_FIELD:
			control = wx.TextCtrl(self.panel)
			self.addControl(field[self.KEY], control)


		sizer = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(label, 0, wx.EXPAND)
		sizer.Add(control, 1, wx.EXPAND | wx.LEFT, 5)

		return sizer


	def addControl(self, key, control):

		if key not in self.controls:
			self.controls[key] = control
		else:
			raise NameError("Existent control key")


	def getControl(self, key):

		return self.controls[key]


	def getControls(self):

		return self.controls
