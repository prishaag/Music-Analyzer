# SI 206 Final Project Report

## Authors
Abigail Cremers, Prisha Agnihotri, William Ward

## Disclaimers 
- The GitHub commit history might be misleading because our team used VSCode Liveshare to work on the project simultaneously on the same files to avoid merge errors. Each team member contributed equally.

### 1. Project Goals 
Our project was centered on music data analysis, utilizing a range of APIs including the Billboard Top 100 Hits, Spotify, and YouTube. Our objective was to compile comprehensive song data in our SQL Database, encompassing titles, ranks, and artists, sourced from the Billboard Top 100 Hits. Additionally, we harnessed the Spotify API (Spotipy) to gather essential song features like danceability and tempo, and we employed the YouTube API to extract statistics on the most popular YouTube videos associated with each song. The primary aim was to conduct a comparative analysis of song characteristics across YouTube, Spotify, and the Billboard Top 100, providing valuable insights into song popularity and attributes. 

### 2. Calculations and Data 
The calculations are included in the repository and code, along with a list of songs and their Spotify statistics.

### 3. Visualization 
Visualization screenshots or image files can be found in the repository.

### 4. Instructions for Running the Code 
1. Clone the GitHub repository.
2. Create a `secrets.json` file with the following format, replacing placeholders with actual keys:
```json
{
    "spotify": {
      "client_id": "addyourkeyhere",
      "client_secret": "addyourkeyhere"
    },
    "youtube": {
      "api_key": "addyourkeyhere"
    },
    "billboard": {
        "X-RapidAPI-Key": "addyourkeyhere",
        "X-RapidAPI-Host": "billboard2.p.rapidapi.com"
    }
}
