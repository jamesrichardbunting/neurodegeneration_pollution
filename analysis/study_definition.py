from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
)

neuro_codes = codelist_from_csv(
    "codelists/opensafely-other-neurological-conditions-2020-06-02.csv",
    system="ctv3",
    column="CTV3ID")

demen_codes = codelist_from_csv(
    "codelists/opensafely-dementia-complete-48c76cf8.csv",
    system="ctv3",
    column="code")

study_codes = combine_codelists(
    neuro_codes,
    demen_codes)

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
                    "int": {"distribution": "population_ages"},},),


    # With one of the codes from the codelists
    clinical_event = patients.with_these_clinical_events(
                    study_codes,
                    between = ["2002-01-01", "today"],
                    returning = "date",
                    find_first_match_in_period = True,
                    return_expectations = {"date": {"earliest": "2002-01-01", "latest": "today"},},),


    # Define the study population
    population = patients.satisfying(
        """
        clinical_event AND registered
        """,
        registered = patients.registered_with_one_practice_between("2002-01-01", "today"),),
    
    # DOB
    dob = patients.date_of_birth(date_format="YYYY-MM",
            return_expectations={
                "date": {"earliest": "1950-01-01", "latest": "today"},
                "rate": "uniform",
                }
        ),

    # Return address information
    msoa = patients.address_as_of("today", returning="msoa"),
    imd = patients.address_as_of("today", 
        returning = "index_of_multiple_deprivation",
        round_to_nearest = 100,
        return_expectations={
            "rate": "universal", 
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7},},},),

)