import logging
import warnings

class DataFilter:

    def account_dim_filter(self, dataframe):
        logging.debug("Filter was calling for function account_dim_filter")
        return dataframe

    def requests_filter(self, dataframe):
        ping = "courses\/\d+\/ping$"
        activity_stream = "courses\/\d+\/activity_stream\/summary$"
        quiz_submission_backup = "courses\/\d+\/quizzes\/\d+\/submissions\/backup\?user_id=\d+.*"
        dataframe = dataframe[(dataframe[5] != "\\N") & (dataframe[6] != "\\N") & (dataframe[22] == "\\N") & (dataframe[27] == "\\N") & (dataframe[13].str.contains(pat=ping)==False) & (dataframe[13].str.contains(pat=activity_stream)==False) & (dataframe[13].str.contains(pat=quiz_submission_backup)==False)]
        del dataframe[22]
        del dataframe[27]
        return dataframe

    def module_item_dim_filter(self, dataframe):
        logging.debug("Filter was calling for function module_item_dim_filter")
        return dataframe[dataframe[10] != 'deleted']
        