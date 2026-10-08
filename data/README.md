# Dataset Documentation

## Primary Dataset Overview
- **Dataset Name**: Datasets for Phishing Websites Detection
- **Authors**: Grega Vrbančič, Iztok Fister Jr., Vili Podgorelec
- **Publication**: *Data in Brief*, Volume 33, Article 106438, December 2020.
- **Publisher**: Elsevier
- **DOI**: [10.1016/j.dib.2020.106438](https://doi.org/10.1016/j.dib.2020.106438)
- **Repository / Source**: [GitHub GregaVrbancic/Phishing-Dataset](https://github.com/GregaVrbancic/Phishing-Dataset)
- **License**: Open Academic Research Data

## Dataset Properties
- **Total Samples**: 58,645 URLs
- **Total Features**: 111 structured URL/domain/directory/file/parameter lexical and structural features
- **Class Label**: `phishing` (Binary: `1` for Phishing, `0` for Legitimate)
- **Class Distribution**:
  - Phishing (1): 30,647 instances (52.26%)
  - Legitimate (0): 27,998 instances (47.74%)
- **Missing Values**: 0 (Complete data matrix)

## Feature Categorization
The 111 features extracted without executing dynamic web code include:
1. **URL-level metrics**: Character counts (`qty_dot_url`, `qty_hyphen_url`, `qty_slash_url`, `qty_and_url`, `qty_equal_url`, etc.), total URL length (`length_url`), TLD counts.
2. **Domain-level metrics**: Domain length, character frequencies in domain name (`qty_dot_domain`, `qty_hyphen_domain`, `qty_vowels_domain`), IP address presence.
3. **Path & Directory metrics**: Directory length, depth (`qty_slash_directory`), special characters in directory path.
4. **File-level metrics**: File name length, extension characteristics.
5. **Parameter/Query metrics**: Query length, number of parameters (`qty_params`), special characters in parameters.
6. **Lookup/Resolver indicators**: Number of resolved IP addresses, TTL, SPF, TLS/SSL flags.

## Data Preprocessing Pipeline
- **Splitting**: Stratified 80% Train (46,916 samples) / 20% Test (11,729 samples) split.
- **Fitting Guarantee**: Preprocessing transformations (scaling, variance filtering) are fitted exclusively on the training set to prevent data leakage.
