import wx
from puzzle import your_function
from puzzle import Colour, LogicGridCell

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100), \
                style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        
        self.width = 5
        self.height = 6
        self.grid = [[LogicGridCell(Colour.NA) for _0 in range(self.width)] for _1 in range(self.height)]

        self.topnav_height = 75
        self.bottomnav_height = 30

        self.buttons = []
        self.topnav_panel = wx.Panel(self)  # Create a panel to place the controls
        self.create_top_controls()  # Call method to create top controls

        self.is_dragging = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_LEFT_UP, self.LeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Show(True)

        self.init_buttons()

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

    def get_cell_height(self) -> int:
        """
        Calculates the cell height
        """
        return int(min(70 - (0.05 * (self.width ** 2)), 70 - (0.05 * (self.height ** 2))))

    def resize_window(self) -> None:
        """
        Resizes the window to fit the cells
        """
        x = self.get_cell_height()
        h = x * self.width
        w = x * self.height
        wx.Window.SetSize(self, h + 16, w + 39 + self.topnav_height + self.bottomnav_height)

    def OnResize(self, event):
        s = self.GetClientSize()
        s[1] = self.topnav_height
        self.topnav_panel.SetSize(s)  # Adjust the panel size to match the frame size
        self.Refresh()  # Refresh the window to redraw the content

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

    def create_button(self, i: int, j: int, cell_height: int | None = None) -> wx.Button:
        """
        Creates an individual button
        """
        if cell_height is None:
            cell_height = self.get_cell_height()
        pos = (cell_height * (i + 1) - 25, cell_height * j + 5 + self.topnav_height)
        btn = wx.Button(self, label="+", size=(20, 20), pos=pos)
        btn.Bind(wx.EVT_BUTTON, self.on_button_click)
        btn.cell_coords = (i, j)
        return btn

    def init_buttons(self) -> None:
        """
        Initialises the buttons
        """
        for i in range(self.width):
            for j in range(self.height):
                self.buttons.append(self.create_button(i, j))

    def create_top_controls(self) -> None:
        self.height_ctrl = wx.TextCtrl(self.topnav_panel, value=str(self.height), style=wx.TE_PROCESS_ENTER, size=(50, -1), pos=(100, 10))

        btn_height_plus = wx.Button(self.topnav_panel, label="+", pos=(45, 10))
        btn_height_plus.Bind(wx.EVT_BUTTON, self.on_increment_height)

        btn_height_minus = wx.Button(self.topnav_panel, label="-", pos=(145, 10))
        btn_height_minus.Bind(wx.EVT_BUTTON, self.on_decrement_height)


        self.width_ctrl = wx.TextCtrl(self.topnav_panel, value=str(self.width), style=wx.TE_PROCESS_ENTER, size=(50, -1), pos=(100, 40))

        btn_plus_width = wx.Button(self.topnav_panel, label="+", pos=(45, 40))
        btn_plus_width.Bind(wx.EVT_BUTTON, self.on_increment_width)

        btn_minus_width = wx.Button(self.topnav_panel, label="-", pos=(145, 40))
        btn_minus_width.Bind(wx.EVT_BUTTON, self.on_decrement_width)

    def move_buttons(self, cell_height: int | None = None) -> None:
        if cell_height is None:
            cell_height = self.get_cell_height()
        for btn in self.buttons:
            i, j = btn.cell_coords
            btn.SetPosition((cell_height * (i + 1) - 25, cell_height * j + 5 + self.topnav_height))

    def nums_modified(self) -> None:
        self.update_number_display()
        self.DoDrawing()
        self.move_buttons()

    def on_increment_height(self, event) -> None:
        self.height += 1
        self.grid.append([LogicGridCell(Colour.NA) for _ in range(self.width)])
        for i in range(self.width):
            self.buttons.append(self.create_button(i, self.height - 1))
        self.nums_modified()

    def on_decrement_height(self, event) -> None: # no good
        if self.height == 1:
            return
        self.height -= 1
        self.grid.pop()
        self.buttons = [b for b in self.buttons if b.cell_coords[1] != self.height]
        self.nums_modified()

    def on_increment_width(self, event) -> None:
        self.width += 1
        for i in range(self.height):
            self.grid[i].append(LogicGridCell(Colour.NA))
            self.buttons.append(self.create_button(self.width- 1, i))
        self.nums_modified()

    def on_decrement_width(self, event) -> None:
        if self.width == 1:
            return
        self.width -= 1
        for i in range(self.height):
            self.grid[i].pop()
        self.buttons.pop()
        self.nums_modified()

    def update_number_display(self) -> None:
        self.height_ctrl.SetValue(str(self.height))
        self.width_ctrl.SetValue(str(self.width))

    def on_button_click(self, event) -> None:
        button = event.GetEventObject()
        coords = button.cell_coords
        coords = (coords[1], coords[0])
        txt = self.grid[coords[0]][coords[1]].inf
        if txt is None:
            txt = ""
        inp = self.show_input_dialog(coords, txt)
        if inp != self.grid[coords[0]][coords[1]].inf or inp is not None:
            self.grid[coords[0]][coords[1]].inf = inp
            self.DoDrawing()

    def show_input_dialog(self, coords: tuple[int, int], default: str = "") -> str | None:
        dlg = wx.TextEntryDialog(self, "Enter value for cell:", f"Cell {coords}", f"{default}")

        user_input = None
        if dlg.ShowModal() == wx.ID_OK:
            user_input = dlg.GetValue()

        dlg.Destroy()
        return user_input

    def draw_grid(self, dc) -> None:
        x = self.get_cell_height()
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)

        for i in range(self.height):
            for j in range(self.width):
                # Draw cell
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                dc.SetBrush(self.brush_colour(self.grid[i][j].col))
                dc.DrawRectangle(x*j,x*i + self.topnav_height,x,x)
                # Draw cell info
                if self.grid[i][j].inf is not None and self.grid[i][j].col != Colour.NA:
                    dc.SetTextForeground(self.text_colour(self.grid[i][j].col))
                    dc.DrawText(self.grid[i][j].inf, int(x * ( j + 0.2)) , int(x *( i + 0.2) + self.topnav_height))

    def click(self, x, y):
        cell_height = self.get_cell_height()
        if x < self.topnav_height:
            return
        x = int((x - self.topnav_height) / cell_height)
        y = int(y / cell_height)
        self.grid[x][y].col = self.get_next_colour(self.grid[x][y].col)
        self.DoDrawing()
        self.is_dragging = True

    def OnClick(self, event):
        y, x = event.GetPosition()
        self.click(x,y)

    def OnDoubleClick(self, event):
        y, x = event.GetPosition()
        self.click(x,y)
        self.click(x,y)

    def LeftUp(self, event):
        self.is_dragging = False



app = wx.App(False)
frame = MyFrame(None, 'Islans of Insight')
app.MainLoop()
