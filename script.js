let movies = [];

async function loadMovies() {
    try {
        const response = await fetch('imdb_top_250.json');
        if (!response.ok) {
            throw new Error('Failed to load JSON data');
        }
        movies = await response.json();

        // convert runtime to minutes
        movies.forEach(movie => {
            movie.runtime = convertRuntimeToMinutes(movie.runtime);
        });

        populateDropdown();
    } catch (error) {
        console.error('Error loading movies:', error);
    }
}


function convertRuntimeToMinutes(runtimeStr) {
    let hours = 0, minutes = 0;

    if (runtimeStr.includes('h')) {
        const [hourPart, minutePart] = runtimeStr.split('h');
        hours = parseInt(hourPart.trim());
        if (minutePart) {
            minutes = parseInt(minutePart.replace('m', '').trim());
        }
    } else if (runtimeStr.includes('m')) {
        minutes = parseInt(runtimeStr.replace('m', '').trim());
    }

    return hours * 60 + minutes;
}

//
function populateDropdown() {
    const movieDropdown = document.getElementById('movieDropdown');
    movies.forEach(movie => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.className = 'dropdown-item';
        a.href = '#';
        a.textContent = movie.title;
        a.onclick = () => handleMovieSelection(movie.title); 
        li.appendChild(a);
        movieDropdown.appendChild(li);
    });
}


function handleMovieSelection(selectedTitle) {
    const selectedMovieDisplay = document.getElementById('selectedMovie');
    selectedMovieDisplay.textContent = `${selectedTitle}`;

    const recommendations = recommendSimilarMovie(selectedTitle);
    displayRecommendations(recommendations);
}

function displayRecommendations(recommendations) {
    const recommendationList = document.getElementById('recommendationList');
    recommendationList.innerHTML = ''; 

    if (recommendations.length === 0) {
        recommendationList.textContent = 'No similar movies found!';
        return;
    }

    recommendations.forEach(title => {
        const li = document.createElement('li');
        li.textContent = title;
        recommendationList.appendChild(li);
    });
}

function recommendSimilarMovie(selectedTitle) {
    let selectedMovie = null;
    for (const movie of movies) {
        if (movie.title === selectedTitle) {
            selectedMovie = movie;
            break;
        }
    }

    if (!selectedMovie) return [];

    const similarMovies = [];

    // recommendation logic conditions
    for (const movie of movies) {
        if (movie.title === selectedTitle) continue;

        if (selectedMovie.content_rating !== "Not Rated" && movie.content_rating !== selectedMovie.content_rating) {
            continue;
        }

        if (Math.abs(movie.imdb_rating - selectedMovie.imdb_rating) > 0.2) {
            continue;
        }

        if (Math.floor(movie.year / 10) !== Math.floor(selectedMovie.year / 10)) {
            continue;
        }

        if (Math.abs(movie.runtime - selectedMovie.runtime) > 30) {
            continue;
        }

        similarMovies.push(movie.title);
    }

    return similarMovies;
}

loadMovies();