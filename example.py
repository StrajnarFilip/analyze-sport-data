from analyze_sport_data import heart_rate_dataframe
from analyze_sport_data.file_records import from_fit_file
from matplotlib.pyplot import show
from os import scandir

data = [
    from_fit_file(file.path, file.name) for file in scandir(".")
    if file.name.endswith(".fit") and file.is_file()
]

heart_rate_dataframe(data).plot()
show()
