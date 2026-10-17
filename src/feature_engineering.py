"""
Feature engineering and taxonomy categorization for URL-based features.
"""

def categorize_features(feature_names):
    """
    Categorize the 111 static features into 6 intuitive security feature families:
    1. URL-Level Lexical Metrics
    2. Domain-Level Structural Metrics
    3. Directory & Path Metrics
    4. File-Level Metrics
    5. Query & Parameter Metrics
    6. Network & Resolver Lookup Metrics
    """
    categories = {
        "URL-Level Lexical": [],
        "Domain-Level": [],
        "Directory & Path": [],
        "File-Level": [],
        "Query & Parameter": [],
        "Resolver & Network": []
    }
    
    for feat in feature_names:
        feat_lower = feat.lower()
        if "_domain" in feat_lower or feat_lower.startswith("domain_"):
            categories["Domain-Level"].append(feat)
        elif "_directory" in feat_lower or feat_lower.startswith("directory_"):
            categories["Directory & Path"].append(feat)
        elif "_file" in feat_lower or feat_lower.startswith("file_"):
            categories["File-Level"].append(feat)
        elif "_params" in feat_lower or feat_lower.startswith("params_"):
            categories["Query & Parameter"].append(feat)
        elif any(k in feat_lower for k in ["ips", "ttl", "spf", "ssl", "tls", "asn", "time_response"]):
            categories["Resolver & Network"].append(feat)
        else:
            categories["URL-Level Lexical"].append(feat)
            
    return categories

def get_feature_descriptions():
    """
    Returns a dictionary of descriptions for key URL features for explainability reporting.
    """
    return {
        "directory_length": "Total character length of the directory path string (deep nesting masks fraud)",
        "time_domain_activation": "Domain registration age in days from WHOIS (new domains strongly signal phishing)",
        "qty_slash_url": "Total count of forward slash ('/') delimiters across entire URL structure",
        "length_url": "Total character length of the raw URL string (long strings evade quick visual audits)",
        "qty_dot_domain": "Number of subdomains/dots inside domain authority (used in multi-level spoofing)",
        "ttl_hostname": "DNS Time-to-Live metric (short TTLs reflect fast-flux evasion infrastructure)",
        "asn_ip": "Autonomous System Number of hosting IP (identifies suspicious hosting providers/ASNs)",
        "time_response": "HTTP lookup response latency in seconds (short-lived rogue hosts vary in latency)",
        "qty_hyphen_directory": "Hyphen occurrences in directory path (used to mimic brand keywords in path)",
        "qty_redirects": "Number of HTTP redirection hops before reaching final target landing page",
        "time_domain_expiration": "Time remaining until domain expiration (throwaway domains have short leases)",
        "qty_nameservers": "Number of authoritative DNS name servers associated with the domain",
        "domain_length": "Total character length of the domain authority string",
        "qty_mx_servers": "Number of configured MX mail exchange servers (legitimate domains configure MX)",
        "qty_dot_url": "Total count of dot ('.') characters across the complete URL string",
        "qty_hyphen_url": "Total count of hyphen ('-') characters across the URL string",
        "qty_underline_url": "Total count of underscore ('_') characters across the URL string",
        "qty_equal_url": "Total count of equality ('=') symbols, typical in credential query arguments",
        "qty_and_url": "Total count of ampersand ('&') symbols separating URL parameters",
        "qty_hyphen_domain": "Hyphens inside domain name (used in typosquatting and brand impersonation)",
        "qty_vowels_domain": "Vowel count in domain name, reflecting phonetic pronounceability vs randomness",
        "qty_dot_directory": "Dots within directory paths (used for masking executable/script extensions)",
        "qty_slash_directory": "Directory path nesting depth across sub-folders",
        "qty_params": "Number of query parameter keys passed in the URL string",
        "qty_ip_resolved": "Number of distinct IP addresses returned by DNS lookup resolution",
        "tls_ssl_certificate": "Presence of a valid TLS/SSL transport security certificate flag"
    }

