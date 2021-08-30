from cohortextractor import combine_codelists

neuro_codes = codelist_from_csv(
    "codelists/opensafely-other-neurological-conditions-2020-06-02.csv",
    system="ctv3",
    column="CTV3ID")

demen_codes = codelist_from_csv(
    "codelists/opensafely-dementia-complete-48c76cf8.csv",
    system="ctv3",
    column="CTV3ID")

study_codes = combine_codelists(
    neuro_codes,
    demen_codes)
