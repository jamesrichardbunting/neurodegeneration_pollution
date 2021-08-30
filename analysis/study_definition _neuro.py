from codelists import *

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
        "incidence": 0.5},
    

    # Define the study index date
    index_date="2002-01-01",


    # Define age
    age = patients.age_as_of("2019-09-01",
                    return_expectations={"rate": "universal",
                    "int": {"distribution": "population_ages"},},)


    # With one of the codes from the codelists
    date_of_clinical_event = patients.with_these_clinical_events(
                    study_codes,
                    between = [index_date, "today"],
                    returning = "date",
                    find_first_match_in_period = True,
                    return_expectations = {"date": {earliest; index_date, "latest": "today"}})


    # Define the study population
    population = patients.satisfying(

        # Registered at same practice since 2002
        registered_with_one_practice_between(index_date, "today"),
        
        # Aged over 60 as of Jan 2002
        age >= 60,

        
        
    )

    # Return address information
    msoa = patients.address_as_of(date_of_clinical_event, returning="msoa", None, return_expectations=None)
    imd = patients.address_as_of(date_of_clinical_event, 
        returning = "index_of_multiple_deprivation",
        round_to_nearest = 100,
        return_expectations={
            "rate": "universal", 
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7}},},)

)