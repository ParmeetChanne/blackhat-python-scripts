import win32gui
import win32ui
import win32con
import win32api

# grab a handle to the main desktop window
hdesktop = win32gui.GetDesktopWindow()

# determine the size of all the monitors in pixels
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# create a device context
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateCompatibleDC()

# create a bitmap object
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy the screen into our memory device context
mem.dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32com.SRCCOPY)

# save the bitmap to a file
screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

# free our objects
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
