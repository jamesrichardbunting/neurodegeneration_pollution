from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
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
        
        registered_with_one_practice_between(
        "2002-01-01", "2020-02-01"
    ),

    age=patients.age_as_of(
        "2019-09-01",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
)