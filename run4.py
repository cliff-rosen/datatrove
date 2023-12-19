from urllib.parse import urlparse, parse_qs

url = "http://www.example.com/path/page?query1=a/b/c&query2=value2#fragment"

# Parse the URL
parsed_url = urlparse(url)

# Access individual components
print(f"Scheme: {parsed_url.scheme}")
print(f"Netloc: {parsed_url.netloc}")
print(f"Path: {parsed_url.path}")
print(f"Params: {parsed_url.params}")
print(f"Query: {parsed_url.query}")
print(f"Fragment: {parsed_url.fragment}")

# Parse query parameters
query_params = parse_qs(parsed_url.query)

print("Query Parameters:")
for key, value in query_params.items():
    print(f"{key}: {value}")
