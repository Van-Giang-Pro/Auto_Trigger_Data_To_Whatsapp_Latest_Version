import pyodbc
import pandas as pd


class SqlServer:
	def __init__(self, site):
		self.site = site
		server = f"Driver=SQL Server;Server={site}MESSQLODS;Database=ODS;Trusted_Connection=Yes"
		self.connection = pyodbc.connect(server)
		self.connection.cursor()

	def data_collection(self, query, start_time, end_time):
		query = query.replace("__SelectedSite__", self.site)\
					.replace("__StartTime__", start_time)\
					.replace("__EndTime__", end_time)
		datacollected = pd.read_sql_query(query, self.connection, index_col=None)


