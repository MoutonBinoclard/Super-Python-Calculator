import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "SPC_fonts/Zoetic.ttf"
custom_font = fm.FontProperties(fname=font_path)

plt.figure()
plt.text(0.5, 0.5, "Test Zoetic", fontproperties=custom_font, fontsize=20, ha='center')
plt.show()