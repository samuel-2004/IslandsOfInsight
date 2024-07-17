import wx
from puzzle import your_function
from puzzle import Colour, LogicGridCell

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100), \
                style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.height = 5
        self.width = 6
        self.buttons = []
        self.grid = [[LogicGridCell(Colour.NA) for i in range(self.height)] for j in range(self.width)]

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Show(True)

        self.create_buttons()

    def brush_colour(self, col: Colour):
        """
        gets the brush for each colour
        """
        if col == Colour.NA:
            return wx.Brush(wx.Colour(50, 50, 50))
        elif col == Colour.WHITE:
            return wx.Brush(wx.Colour(255,255,255))
        elif col == Colour.BLACK:
            return wx.Brush(wx.Colour(0,0,0))
        elif col == Colour.EMPTY:
            return wx.Brush(wx.Colour(100,100,100))

    def text_colour(self, colour_of_cell: Colour) -> Colour:
        """
        What colour should the text be based on the cell colour
        """
        if colour_of_cell == Colour.NA or colour_of_cell == Colour.BLACK:
            return wx.Colour(255,255,255)
        else:
            return wx.Colour(0,0,0)

    def get_cell_width(self):
        return int(min(70 - (0.05 * (self.height ** 2)), 70 - (0.05 * (self.width ** 2))))

    def resize_window(self):
        x = self.get_cell_width()
        h = x * self.height
        w = x * self.width
        wx.Window.SetSize(self, h + 16, w + 39)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.DoDrawing(dc)

    def DoDrawing(self, dc=None):
        if dc is None:
            dc = wx.ClientDC(self)

        self.resize_window()
        self.draw_grid(dc)

    def get_next_colour(self, col : Colour) -> Colour:
        """
        gets the next colour
        """
        if col == Colour.NA:
            return Colour.WHITE
        elif col == Colour.WHITE:
            return Colour.BLACK
        elif col == Colour.BLACK:
            return Colour.EMPTY
        elif col == Colour.EMPTY:
            return Colour.NA

    def create_buttons(self):
        for i in range(self.height):
            row_buttons = []
            for j in range(self.width):
                btn = wx.Button(self, label="+", size=(30, 30), pos=(self.get_cell_width() * i + self.get_cell_width() - 35, self.get_cell_width() * j + 5))
                btn.Bind(wx.EVT_BUTTON, self.on_button_click)
                btn.cell_coords = (i, j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_button_click(self, event) -> None:
        button = event.GetEventObject()
        coords = button.cell_coords
        txt = self.grid[coords[0]][coords[1]].inf
        if txt is None:
            txt = ""
        inp = self.show_input_dialog(coords, txt)
        if inp is not None:
            self.grid[coords[0]][coords[1]].inf = inp

    def show_input_dialog(self, coords: tuple[int, int], default: str = "") -> str | None:
        dlg = wx.TextEntryDialog(self, "Enter value for cell:", f"Cell {coords}", f"{default}")

        user_input = None
        if dlg.ShowModal() == wx.ID_OK:
            user_input = dlg.GetValue()

        dlg.Destroy()
        return user_input

    def draw_grid(self, dc) -> None:
        x = self.get_cell_width()
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)

        for i in range(self.width):
            for j in range(self.height):
                # Draw cell
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                dc.SetBrush(self.brush_colour(self.grid[i][j].col))
                dc.DrawRectangle(x*j,x*i,x,x)
                # Draw plus icon
                self.draw_plus_icon(dc, x * j, x * i, x)
                # Draw cell info
                if self.grid[i][j].inf is not None and self.grid[i][j].col != Colour.NA:
                    dc.SetTextForeground(self.text_colour(self.grid[i][j].col))
                    dc.DrawText(self.grid[i][j].inf, int(x * ( j + 0.2)) , int(x *( i + 0.2)))

    def draw_plus_icon(self, dc, x, y, cell_size):
        plus_size = cell_size // 5
        half_plus = plus_size // 2

        dc.SetPen(wx.Pen(wx.Colour(90, 90, 90), 2))  # Grey color for plus icon
        center_x = x + cell_size - half_plus - 5  # Adjust the position slightly
        center_y = y + half_plus + 5  # Adjust the position slightly

        # Vertical line of plus
        dc.DrawLine(center_x, center_y - half_plus, center_x, center_y + half_plus)
        # Horizontal line of plus
        dc.DrawLine(center_x - half_plus, center_y, center_x + half_plus, center_y)

    def click(self, x, y):
        cell_width = self.get_cell_width()
        x = int(x / cell_width)
        y = int(y / cell_width)
        self.grid[x][y].col = self.get_next_colour(self.grid[x][y].col)
        self.DoDrawing()

    def OnClick(self, event):
        y, x = event.GetPosition()
        self.click(x,y)

    def OnDoubleClick(self, event):
        y, x = event.GetPosition()
        self.click(x,y)
        self.click(x,y)



app = wx.App(False)
frame = MyFrame(None, 'Islans of Insight')
app.MainLoop()
