import sys
import os
from collections import defaultdict
import json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <base_dir>")
        sys.exit(1)
    if not os.path.isdir(basedir := sys.argv[1]):
        print(f"{basedir} is not a valid directory.")
        sys.exit(1)

    # dir_name to category string
    categ_dict = {
        "distrib": "分散システム",
        "storage": "ストレージ",
        "virtual": "コンテナ・VM",
        "linux": "Linux",
        "etc": "未分類",
    }
    top_title = "#+TITLE: Personal Wiki Index"

    # Read config.json
    try:
        with open("/".join([basedir, "config.json"])) as f:
            config = json.load(f)
            top_title = "#+TITLE: " + config.pop("#+TITLE", top_title)
            categ_dict = config
    except Exception:
        print("Skip loading config.json")

    # Save README.org if exists
    readme_path = "/".join([basedir, "README.org"])
    readme_bk_path = readme_path + ".bk"
    try:
        os.remove(readme_bk_path)
    except Exception:
        pass
    if os.path.exists(readme_path):
        os.rename(readme_path, readme_bk_path)

    # Create org_dic
    #   category_string: list of (full_path, title) tuples
    #   Note: multiple categories could share the same category_string
    org_dic = defaultdict(list)
    for (dpath, _, fnames) in os.walk(basedir):
        for fname in fnames:
            if fname.endswith(".org"):
                full_path = "/".join([dpath, fname])
                categ = categ_str = dpath[dpath.rfind("/") + 1 :].lower()
                try:
                    categ_str = categ_dict[categ]
                except Exception:
                    pass
                with open(full_path, "r") as f:
                    title = "No #+TITLE: header!"
                    for line in f:
                        title_head = "#+TITLE: "
                        if line.startswith(title_head):
                            title = line[len(title_head) :].rstrip()
                            break
                link_path = "." + full_path[len(basedir) :]
                org_dic[categ_str].append((link_path, title))

    # Generate README.org based on org_dic
    with open(readme_path, "w") as f:
        print(top_title, file=f)
        print("\nPersonal memos\n", file=f)
        for categ_str, link_list in org_dic.items():
            print(f"** {categ_str}", file=f)
            print("", file=f)
            for link in link_list:
                print(f"- [[{link[0]}][{link[1]}]]", file=f)
            print("", file=f)
