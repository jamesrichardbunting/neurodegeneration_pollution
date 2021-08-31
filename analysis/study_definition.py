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
        "date": {"earliest": "1900-01-01", "latest": "2020-01-01"},
        "rate": "uniform",
        "incidence": 0.5},
    

    # Define the study index date
    index_date="2002-01-01",


    # Define the study population
    population = patients.satisfying(
        
        """
        static_patient AND clinical_event AND (age_in_2002 > 59)
        """,

        # Registered with one practice since 1992
        static_patient = patients.registered_with_one_practice_between("1992-01-01", "2020-01-01"),

        # With one of the codes
        clinical_event = patients.with_these_clinical_events(
            study_codes,
            between = ["2002-01-01", "2020-01-01"]),

        # Aged >= 60 as of 2002
        age_in_2002 = patients.age_as_of("2002-01-01",
            return_expectations={
                "rate" : "universal",
                "int" : {"distribution" : "population_ages"},},),),


    # Date of clinical event (codes from the codelists)    
    clinical_event_date = patients.with_these_clinical_events(    
        study_codes,
        between = ["2002-01-01", "2020-01-01"],
        returning = "date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period = True,
        return_expectations = {"date": {"earliest": "2002-01-01", "latest": "2020-01-01"},},),

    
    # Clinical event code (codes from the codelists)    
    clinical_event_code = patients.with_these_clinical_events(    
        study_codes,
        between = ["2002-01-01", "2020-01-01"],
        returning = "code",
        find_first_match_in_period = True,
        return_expectations = {
            "rate": "universal", 
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7},},},),


    # Age at clinical event
    age = patients.age_as_of("clinical_event_date",
            return_expectations={
                "rate" : "universal",
                "int" : {"distribution" : "population_ages"},},),
    

    # Return address information
    imd = patients.address_as_of("clinical_event_date", 
        returning = "index_of_multiple_deprivation",
        round_to_nearest = 100,
        return_expectations={
            "rate": "universal", 
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7},},},),


    msoa = patients.address_as_of("clinical_event_date",
        returning="msoa",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {},},},)
)