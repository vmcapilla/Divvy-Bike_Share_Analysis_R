import pyautogui


fw = pyautogui.getAllWindows()



for i in range (len(fw)):
	if ('Google Chrome' in fw[i].title):
		print(fw[i].title)
		pyautogui.doubleClick(fw[i].left+10, fw[i].top+10)
		break
	else:
		pass