import os
import csv
import wave

# Change this to the location of your QariGuard-Dataset folder
BASE_DIR = r"C:\Users\DELTA\Desktop\QariGuard-DigitalQuranCompute\Code\QariGuard-Dataset"

OUTPUT_FILE = os.path.join(BASE_DIR, "dataset_metadata.csv")

rows = []

folders = [
    ("Authentic", "authentic"),
    ("Synthetic", "synthetic")
]

for folder_name, label in folders:

    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue

    for root, dirs, files in os.walk(folder_path):

        for filename in files:

            if not filename.lower().endswith(".wav"):
                continue

            file_path = os.path.join(root, filename)

            # Remove extension
            name = os.path.splitext(filename)[0]

            # Example:
            # 1_AbdulBasit-AbdulSamad_Real
            # 1_AbdulBasit-AbdulSamad_Fake

            parts = name.split("_")

            # Surah number
            surah = parts[0]

            # Reciter name
            reciter_parts = parts[1:-1]
            reciter = " ".join(reciter_parts)

            # Audio information
            duration = ""
            sample_rate = ""

            try:
                with wave.open(file_path, "rb") as audio:

                    frames = audio.getnframes()
                    sample_rate = audio.getframerate()

                    if sample_rate > 0:
                        duration = round(frames / sample_rate, 3)

            except Exception as e:
                print(f"Could not read audio information: {filename}")
                print(e)

            # Generation method
            if label == "synthetic":
                generation_method = "ElevenLabs"
                source = "AI-generated"
            else:
                generation_method = ""
                source = "Authentic recording"

            rows.append([
                filename,
                label,
                reciter,
                surah,
                duration,
                sample_rate,
                generation_method,
                source
            ])


# Write CSV file
with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "file_name",
        "label",
        "reciter",
        "surah",
        "duration_seconds",
        "sample_rate_hz",
        "generation_method",
        "source"
    ])

    writer.writerows(rows)


print()
print("========================================")
print("Metadata file created successfully!")
print("========================================")
print(f"Number of files: {len(rows)}")
print(f"Output: {OUTPUT_FILE}")