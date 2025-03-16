from analyze_sport_data import heart_rate_dataframe
from analyze_sport_data.file_records import from_fit_file, from_tcx_file
from matplotlib.pyplot import show
from os import scandir

fit_data = [
    from_fit_file(file.path, file.name) for file in scandir(".")
    if file.name.lower().endswith(".fit") and file.is_file()
]

tcx_data = [
    from_tcx_file(file.path, file.name) for file in scandir(".")
    if file.name.lower().endswith(".tcx") and file.is_file()
]

data = fit_data + tcx_data

heart_rate_dataframe(data).plot()
show()
