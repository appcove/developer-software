from packages import *

# if all(isinstance(n, AdsPackage) for n in packages):
#     install_rust()
#     Path(f'temp').mkdir(parents=True, exist_ok=True)

#     cached_submodules_hashes = AdsPackager.get_cached_tools()
#     print(cached_submodules_hashes)

#     for tool in packages:

#         if tool.is_cached(cached_submodules_hashes):
#             print(f"########## {tool.package_name} from cache")
#             subprocess.run(
#                 f"git checkout remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 -- $(git ls-tree --name-only -r remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 | egrep -e '^.*{tool.package_name}.*.deb$')", shell=True)
#             for deb_file in glob.glob(r'*.deb'):
#                 shutil.move(deb_file, "temp")
#         else:
#             print(f"########## {tool.package_name} Building...")
#             tool.build()
#             cached_submodules_hashes[tool.package_name] = AdsPackage.get_current_submodule_hash(
#                 tool.package_name)

#         with open(r'cache.yaml', 'w+', encoding='utf8') as cache_file:
#             yaml.dump(cached_submodules_hashes, cache_file)
