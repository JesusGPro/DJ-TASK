versions_list = ['1.2', '1.2.1', '1.2.2', '2.2', '2', '1.1', '1', '2.1']
wps = ['WP1.1.1:', 'WP1.1.2:', 'WP1.1.3:', 'WP1.1.4:', 'WP1.1:', 'WP1.2.1.1.1:', 'WP1.2.1.1.2:', 'WP1.2.1.1.3:', 'WP1.2.1.1.4:', 'WP1.2.1.1:', 'WP1.2.1.2.1:', 'WP1.2.1.2.2:', 'WP1.2.1.2.3:', 'WP1.2.1.2.4:', 'WP1.2.1.2.5:', 'WP1.2.1.2:', 'WP1.2.1:', 'WP1.2:', 'WP1:']
versions_list = [s.replace('WP', '') for s in wps]
versions_list = [s.replace(':', '') for s in versions_list]
print(versions_list)
# Sort the versions list

sorted_versions = sorted(versions_list, key=lambda x: list(map(int, x.split('.'))))

print(sorted_versions)