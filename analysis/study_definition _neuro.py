from codelists import *

from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
)

neuro_codes = codelist_from_csv(
    "codelists/opensafely-chronic-cardiac-disease.csv", system="ctv3", column="CTV3ID"
)

study = StudyDefinition(
    
    # Define default dummy data behaviour
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    
    # Define the study index date
    index_date="2020-01-01",

    # Define the study population
    population=patients.satisfying(

        "Registered at same practice since 2002 AND over 60 AND Parkinson's, Alzheimer's or dementas = (T OR N)"
        
        registered_with_one_practice_between("2002-01-01", "2020-02-01"),

        age_as_of("2019-09-01",
            return_expectations={"rate": "universal",
                                "int": {"distribution": "population_ages"},},),

        neuro_codes = []

        with_these_clinical_events(
            copd_codes,
            returning = "binary_flag",
            find_first_match_in_period = True,
            between = [index_date, "today"],
            return_expectations = {"incidence": 0.2},),

            haem_cancer_codes,
            between=["2015-03-01", "2020-02-29"],
            returning="date",
            find_first_match_in_period=True,
            return_expectations={"date": {earliest; "2015-03-01", "latest": "2020-02-29"}},
    )

)