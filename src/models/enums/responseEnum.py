from enum import Enum

class ResponseEnum(Enum):
    dataAddedSuccessfully = "the data have been added"
    dataAddedError = "error while adding data"
    validationPassed= " validation Passed"
    validationError= " validation Error"
    dataDeletedSuccessfully = "Data deleted successfully"
    dataDeletedError = "Failed to delete data"
    dataNotFound = "Data not found"
    dataFetchError= "data Fetch Error"
    dataFetchedSuccessfully= "data Fetched Successfully"