import pandas as pd
import matplotlib.pyplot as plt

csv_file = r'C:\Users\bensc\PycharmProjects\scikit\to_image\tracking\final_position_results.csv'
df = pd.read_csv(csv_file)
df = df.drop_duplicates()

print(df)
obj = 2
filtered_df = df.loc[(df['object_id'] == obj)]
print(filtered_df)
plt.plot(filtered_df['x_pos'], filtered_df['y_pos'], linewidth=5)



# title = 'Substrate Fluorescence Response\nat Varied MMP-9 Concentrations'
xaxis = 'x_pos'
yaxis = 'y_pos'

#Font
# font = {'size': 20, 'fontweight':'bold'} #BOLD Version
font = {'size': 18}

#Change title
# plt.title(title, fontdict = font)

#Change axis labels
plt.xlabel(xaxis, fontdict = font)
plt.ylabel(yaxis, fontdict = font)
plt.show()


# TODO: Figure out how to track trajectories from entire video. Not just finishing positions