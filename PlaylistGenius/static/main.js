const BASE_URL = 'http://localhost:5000';

// Make an API call that will some songs to the playlist
async function saveToPlaylist({artist, track}) {
    // const artist = 'atmosphere';
    // const track = 'sunshine';

    try {
        const response = await axios.post(`${BASE_URL}/playlists/add`, {
            artist,
            track
        });
        // show success if response is successful? 
        console.log(response.status);
    } catch(err) {
        // means the api call failed .. somehow?
        // maybe display something to the user that we were unable to save to playlist
        console.error(`ERROR: Unable to save to playlist: track: ${track}, artist: ${artist} : ${err}`);
    } 
}

// Get all tracks that have been selected by the user
function findFavoriteTracks() {
    // get all elements that have the .favoriteTrack class
    const favorite = document.getElementsByClassName('favoriteTrack')
    
    // const favArray = [];

    // for (const fav of favorite) {
    //     // Of those, find which checkboxes are in a selected state
    //     if (fav.checked) {
    //         // log those selected tracks
    //         const artist = fav.getAttribute('data-artist');
    //         const track = fav.getAttribute('data-track');
    //         console.log(artist, track)
    //         favArray.push({ artist, track });
    //     }
    // }

    return [...favorite]
    // Of those, find which checkboxes are in a selected state
    .filter(fav => fav.checked)
    // return new object with artist and track
    .map(fav => ({ artist: fav.getAttribute('data-artist'), track: fav.getAttribute('data-track')}) );
}

function start() {
    document.getElementById('save').addEventListener("click", (e) => {
        e.preventDefault();
        const trackArray = findFavoriteTracks();

        trackArray.forEach(track => saveToPlaylist(track) )
    })
}

window.addEventListener('DOMContentLoaded', start);