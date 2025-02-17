import codecs
import csv
import traceback
import pandas as pd

from CustomErrors import *


class UploadSampleId:
    def __init__(self, cursor, uploader, sampleIdReader):
        self.cursor = cursor
        self.uploader = uploader
        self.sampleIdReader = sampleIdReader
        self.ableToOpenFile = True
        self.noErrors = 0
        self.df = None

        # open the file here, keep it on record
        try:
            self.file = codecs.open(self.sampleIdReader.filePath, "r", encoding="utf-8", errors="ignore")
            self.reader = csv.reader(self.file)

        except:
            self.ableToOpenFile = False


    def uploadBatch(self):
        # have the reader read the batch (# hand it the headers so it can read where they are)
        # get the haders

        if self.ableToOpenFile:
            # try: #FIXME: put this back
                warningRow = next(self.reader)
                headers = list(next(self.reader))
                self.sampleIdReader.readBatch(headers)
            # except:
            #     raise UnableToParseFile(self.sampleIdReader.fileName)
        else:
            raise UnableToOpenFile(self.sampleIdReader.fileName)
        # no need to upload anything else


    # check if a site already exists on the database
    def rowIsUnique(self):
        sqlUnique = "SELECT sort_chem FROM sort_chems WHERE sort_chem = ?;"
        uniqueTuple = (self.sampleIdReader.sortChem,)

        self.cursor.execute(sqlUnique, uniqueTuple)
        result = self.cursor.fetchall()
        if len(result) > 0:
            return False
        else:
            return True
 
    def updateRow(self):
        # modify the row that is already there
        sqlUpdate = "UPDATE sort_chems SET project_id = ?, device = ?, date_sampled=?," \
                    "site_id = ?, time_sampled = ?, sort_chem = ?," \
                    "temperature = ?, pressure = ?, o2_percent = ?," \
                    "o2_mg = ?, conductance = ?, ph = ?, " \
                    "orp = ?, chlorophyl_ugl = ?, chlorophyl_rfu =  ?," \
                    "pc_ug = ?, volume_filtered = ?, calibrated = ?," \
                    "q_salt_grams = ?, q_time = ?, notes = ?, " \
                    "samplers = ?, aqualog_yes = ?, doc_isotopes_yes = ?, " \
                    "elementar_yes = ?, scan_yes = ?, ic_yes = ?," \
                    "icp_yes = ?, lachat_yes = ?, no3_isotopes_yes = ?," \
                    "srp_yes = ?, water_isotopes_yes = ?, tss_yes = ?, ignore_yes = ?," \
                    "datetime_uploaded = ?, file_path = ? WHERE sort_chem = ?;"

        updateTuple = (
            self.sampleIdReader.project, self.sampleIdReader.device, self.sampleIdReader.date,
            self.sampleIdReader.site, self.sampleIdReader.time, self.sampleIdReader.sortChem,
            self.sampleIdReader.temp, self.sampleIdReader.press, self.sampleIdReader.o2percent,
            self.sampleIdReader.o2mg, self.sampleIdReader.cond, self.sampleIdReader.ph,
            self.sampleIdReader.orp, self.sampleIdReader.chlUGL, self.sampleIdReader.chlRFU,
            self.sampleIdReader.pcUG, self.sampleIdReader.volumeFiltered, self.sampleIdReader.cal,
            self.sampleIdReader.qsalt, self.sampleIdReader.qtime, self.sampleIdReader.notes,
            self.sampleIdReader.samplers, self.sampleIdReader.aqualog, self.sampleIdReader.doc,
            self.sampleIdReader.elementar, self.sampleIdReader.scan, self.sampleIdReader.ic,
            self.sampleIdReader.icp, self.sampleIdReader.lachat, self.sampleIdReader.no3,
            self.sampleIdReader.srp, self.sampleIdReader.water, self.sampleIdReader.tss, self.sampleIdReader.ignore,
            self.sampleIdReader.datetimeUploaded, self.sampleIdReader.filePath, self.sampleIdReader.sortChem)

        if self.sampleIdReader.sortChem == "2022-0035":
            print("HEERRREE")

        print(self.sampleIdReader.sortChem)

        self.cursor.execute(sqlUpdate, updateTuple)

    def uploadRow(self):

        sqlInsert = "INSERT INTO sort_chems (project_id, device, date_sampled," \
                    "site_id, time_sampled, sort_chem," \
                    "temperature, pressure, o2_percent," \
                    "o2_mg, conductance, ph, " \
                    "orp, chlorophyl_ugl, chlorophyl_rfu," \
                    "pc_ug, volume_filtered, calibrated," \
                    "q_salt_grams, q_time, notes, " \
                    "samplers, aqualog_yes, doc_isotopes_yes, " \
                    "elementar_yes, scan_yes, ic_yes," \
                    "icp_yes, lachat_yes, no3_isotopes_yes," \
                    "srp_yes, water_isotopes_yes, tss_yes, ignore_yes," \
                    "datetime_uploaded, file_path) " \
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?," \
                    "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?," \
                    "?,?,?,?,?,?,?, ?,?,?);"

        insertTuple = (self.sampleIdReader.project, self.sampleIdReader.device, self.sampleIdReader.date,
            self.sampleIdReader.site, self.sampleIdReader.time, self.sampleIdReader.sortChem,
            self.sampleIdReader.temp, self.sampleIdReader.press, self.sampleIdReader.o2percent,
            self.sampleIdReader.o2mg, self.sampleIdReader.cond, self.sampleIdReader.ph,
            self.sampleIdReader.orp, self.sampleIdReader.chlUGL, self.sampleIdReader.chlRFU,
            self.sampleIdReader.pcUG, self.sampleIdReader.volumeFiltered, self.sampleIdReader.cal,
            self.sampleIdReader.qsalt, self.sampleIdReader.qtime, self.sampleIdReader.notes,
            self.sampleIdReader.samplers, self.sampleIdReader.aqualog, self.sampleIdReader.doc,
            self.sampleIdReader.elementar, self.sampleIdReader.scan, self.sampleIdReader.ic,
            self.sampleIdReader.icp, self.sampleIdReader.lachat, self.sampleIdReader.no3,
            self.sampleIdReader.srp, self.sampleIdReader.water, self.sampleIdReader.tss, self.sampleIdReader.ignore,
            self.sampleIdReader.datetimeUploaded, self.sampleIdReader.filePath)

        self.cursor.execute(sqlInsert, insertTuple)
        
    def fillBlankEvents(self):
        self.df = pd.read_csv(self.filePath, skiprows=1)
        site_df = pd.read_csv(os.path.join(os.getcwd(), "MasterSiteListDescription.csv"))
        uvu_sites = sdf["site_id"][site_df["project_uvu"] == 1].values.tolist()

        dups = df.duplicated(subset=['Temp(Celsius)', 'Pressure', 'DO%', 'DO(mg/L)', 'SPConductivity(uS/cm)', 'pH'])
        df["duplicate"] = dups
        df['counts'] = df[~dups].groupby(['Date(mo/dy/year)', 'Samplers'])['Site'].transform('count')
        df['count_by_site'] = df[~dups].groupby(['Date(mo/dy/year)'])['Site'].transform('count')
        df['counts_no_dups'] = df.groupby(['Date(mo/dy/year)', 'Samplers'])['Site'].transform('count')

        df["sampling"] = [None] * len(df)
        df["sampling"] = df["sampling"].where(~((df["count_by_site"] < 30.5) & (~df["count_by_site"].isna())), "baseline")
        df["sampling"] = df["sampling"].where(~((df["count_by_site"] > 30.5) & (~df["count_by_site"].isna())), "synoptic")
        df["sampling"] = df["sampling"].where(~((df["Site"].isin(uvu_sites))), "uvu")

        # fill errant synoptic sites and dates
        synoptic_dates = []
        for i, r in df.iterrows():
            if r["sampling"] == "synoptic":
                synoptic_dates.append(r["Date(mo/dy/year)"])

        for i, r in df.iterrows():
            if (r["sampling"] == "baseline" and r["Date(mo/dy/year)"] in synoptic_dates) or (
                    type(r["Site"]) == str and "NBS." in r["Site"] and r["sampling"] == "baseline"):
                df.at[i, "sampling"] = "synoptic"

        # catch samples w/o point measurements
        samples_dict = {}
        for i, r in df.iterrows():
            if r["sampling"] is not None and r["Samplers"] != 'THESE ARE DUPLICATES OF THE SYNOPTIC SAMPLING' and type(
                    r["Samplers"]) == str:
                samples_dict[f"{r['Date(mo/dy/year)']}_{r['Samplers']}"] = r["sampling"]

        for i, r in df.iterrows():
            if r["sampling"] is None and r["Event type (Synoptic/UVU/Baseline)"] is None:
                if f"{r['Date(mo/dy/year)']}_{r['Samplers']}" in samples_dict.keys():
                    df.at[i, "sampling"] = samples_dict[f"{r['Date(mo/dy/year)']}_{r['Samplers']}"]

        # catch last baseline samples w/o point measurements
        df["sampling"] = df["sampling"].where(
            ~((df["counts_no_dups"] < 10) & (df["Event type (Synoptic/UVU/Baseline)"].isna())), "baseline")

        # fill empty Event Type rows with best guess
        for i, r in df.iterrows():
            if r["Event type (Synoptic/UVU/Baseline)"] is None:
                if r["sampling"] is not None:
                    df.at[i, "Event type (Synoptic/UVU/Baseline)"] = r["sampling"]

    def uploadReads(self):
        self.rowsMissingValues = []
        self.rowsNoZeroOne = []
        self.rowsRepeated = []
        # FIXME automate fill blank tests
        # self.fillBlankEvents()

        # cycle through each row
        i = 0
        try:
            for row in self.reader: # the first and header row have already been consumed, so this starts right on the correct row
                result = self.sampleIdReader.readRow(row)
                if result == self.sampleIdReader.noError:
                    # check to make sure the row hasn't been uploaded already
                    if (not self.uploader.allowDuplicates) and (not self.rowIsUnique()):
                        self.rowsRepeated.append(i + 2)
                    elif (not self.rowIsUnique()) and self.uploader.allowDuplicates:
                        self.updateRow()
                    else:
                        self.uploadRow()

                elif result == self.sampleIdReader.missingValues:
                    self.rowsMissingValues.append(i + 3)
                elif result == self.sampleIdReader.noZeroOrOne:
                    self.rowsNoZeroOne.append(i + 3)
                i = i + 1

            message = ""
            if len(self.rowsMissingValues) > 0:
                message = message + "ERROR: rows " + str(self.rowsMissingValues) + " were not" \
                                   " uploaded to the database because they were missing values that cannot be empty.\n"
            if len(self.rowsNoZeroOne) > 0:
                message = message + "ERROR: rows " + str(self.rowsNoZeroOne) + " were not uploaded to the " \
                                    "database because they contained a value other than 0 or 1 in the test_yes columns." \
                                    " The purpose of these columns is to indicate which test should (with a 1) and should not (with a 0)" \
                                    " be run on the sample represented by that row.\n"
            if len(self.rowsRepeated) > 0:
                message = message + "ERROR: rows " + str(self.rowsRepeated) + " were not uploaded to the database because " \
                                    "they were duplicates of a row/sort-chem already present on the database. This may be because" \
                                    " tests involving these sort chems have already been uploaded before this sheet was uploaded. " \
                                    "In this case, the values in the sort_chems table for these rows would likely be blank, and you " \
                                    "have little to worry about overriding them. " \
                                    "If you wish to override the values in the sort_chem table for these rows, then please hit the" \
                                    " \'allow duplicates\' button and re-submit this file. Thank you.\n"

            if message != "":
                raise SortChemProblemRows(message, self.sampleIdReader.fileName)
        except:
            print(traceback.format_exc())


