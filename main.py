# This entrypoint file to be used in development. Start by reading README.md
import medical_data_visualizer
from unittest import main

# Draw categorical plot
cat_plot = medical_data_visualizer.draw_cat_plot()
cat_plot.savefig('catplot.png')

# Draw heatmap
heat_map = medical_data_visualizer.draw_heat_map()
heat_map.savefig('heatmap.png')

# Run unit tests automatically
main(module='test_module',exit=False)