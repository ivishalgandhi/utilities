import os
import glob
import argparse
from datetime import datetime

def combine_markdown_files(directory, file_pattern, combined_file, created_after=None, exclude_frontmatter=False):
    # Initialize an empty list to store the contents of the markdown files
    markdown_contents = []

    # Use the glob library to find all files in the specified directory that match the given file pattern
    for filename in glob.glob(os.path.join(directory, file_pattern), recursive=True):
        create_time = datetime.fromtimestamp(os.path.getctime(filename))

        if created_after:
            if create_time < created_after:
                continue
        with open(filename, 'r') as file:
            # Read the contents of the file
            contents = file.read()
            if exclude_frontmatter:
                # Split the contents of the file into the frontmatter and the rest of the content
                frontmatter, content = contents.split("—-", 1)
            else:
                content = contents
            # Add the file name and create date as an h2 header at the top of the content
            content = f"## {os.path.basename(filename)} ({create_time.strftime('%Y-%m-%d')})\n\n{content}"
            # Add the contents of the file to the list
            markdown_contents.append(content)

    # Combine all the contents of the markdown files into a single string
    combined_contents = "\n".join(markdown_contents)

    # Write the combined contents to a new file
    with open(combined_file, 'w') as file:
        file.write(combined_contents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory to search for markdown files")
    parser.add_argument("file_pattern", help="pattern to match markdown file name")
    parser.add_argument("combined_file", help="combined markdown file name")
    parser.add_argument("-c", "--created_after", help="include files created after this date in yyyy-mm-dd format")
    parser.add_argument("-ef", "--exclude_frontmatter", help="exclude frontmatter from markdown files", action="store_true")
    args = parser.parse_args()
    if args.created_after:
        created_after = datetime.strptime(args.created_after, '%Y-%m-%d')
    else:
        created_after = None
    combine_markdown_files(args.directory, args.file_pattern, args.combined_file, created_after, args.exclude_frontmatter)
