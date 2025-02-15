document.addEventListener("DOMContentLoaded", function() {
    fetchCityHighlights();
})

function fetchCityHighlights() {
    fetch('/api/city_highlights')
        .then(response => response.json())
        .then(data => {
            const videoContainer = document.getElementById("video-container");
            videoContainer.innerHTML = "";

            data.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.className = "col-md-4";

                videoCard.innerHTML = `
                   <div class="card mb-3">
                        <img src="${video.thumbnail}" class="card-img-top" alt="${video.title}">
                        <div class="card-body">
                            <h5 class="card-title">${video.title}</h5>
                            <div class="embed-responsive embed-responsive-16by9">
                                <iframe class="embed-responsive-item" src="${video.video_url}" allowfullscreen></iframe>
                            </div>
                        </div>
                    </div>
                `;
                videoContainer.appendChild(videoCard);
            });
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });
}


fetch('/api/squad')
    .then(response => response.json())
    .then(data => {
        // If the data contains an error, display it
        if (data.error) {
            document.getElementById('team-standings').innerHTML = `<p>${data.error}</p>`;
            return;
        }

        const squadDetails = data.team_squad;
        const tableBody = document.getElementById('squad-details');

        squadDetails.forEach((player, index) => {
            const tableBodyRow = document.createElement('tr');

            const tableRowHead = document.createElement('th');
            tableRowHead.setAttribute('scope', 'row');
            tableRowHead.textContent = index+1;

            const tableRowContent1 = document.createElement('td');
            const tableRowContent2 = document.createElement('td');
            const tableRowContent3 = document.createElement('td');

            tableRowContent1.textContent = player[0];
            tableRowContent2.textContent = player[1];
            tableRowContent3.textContent = player[2];

            tableRowContent1.setAttribute('colspan', '2');

            tableBodyRow.appendChild(tableRowHead);
            tableBodyRow.appendChild(tableRowContent1);
            tableBodyRow.appendChild(tableRowContent2);
            tableBodyRow.appendChild(tableRowContent3);
            
            tableBody.appendChild(tableBodyRow);
        });
    })
    .catch(error => {
        console.error('Error fetching matches:', error);
    });

/*--------------------------------------------------------Pl Stats--------------------------------------------------------*/
document.getElementById('pl-button').addEventListener("click", function(event) {
    event.preventDefault();

    fetch('/api/team_data')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('team-standings').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const teamStandings = document.getElementById('team-standings');
            teamStandings.innerHTML = `
                <p><strong>Position:</strong> ${data.position}</p>
                <p><strong>Points:</strong> ${data.points}</p>
                <p><strong>Games Played:</strong> ${data.played_games}</p>
                <p><strong>Won:</strong> ${data.won}</p>
                <p><strong>Draw:</strong> ${data.draw}</p>
                <p><strong>Lost:</strong> ${data.lost}</p>
                <p><strong>Goals For:</strong> ${data.goals_for}</p>
                <p><strong>Goals Conceded:</strong> ${data.goals_conceded}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching team data:', error);
        });

    fetch('/api/pl_team_top_scorer')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('player-name').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const playerScore = data.player_score;

                let maxGoals = -Infinity;
                let topScorerName = '';

                Object.keys(playerScore).forEach(player => {
                    const goals = playerScore[player][0];
                    if (goals > maxGoals) {
                        maxGoals = goals;
                        topScorerName = player;
                    }
                });

                const topScorer = document.getElementById('player-name');
                topScorer.innerHTML = `
                <p>Team Top Scorer: ${topScorerName}</p>
                `;

                const nameParts = topScorerName.split(" ");
                const lastName = nameParts.at(-1).toLowerCase();
                const imageFileName = `${lastName}.jpg`;

                const baseImageURL = '/static/assets/players/';

                const fullImageURL = baseImageURL + imageFileName;
                document.getElementById('top-scorer-img').src = fullImageURL;

                const mostGoals = document.getElementById('goals');
                mostGoals.innerHTML = `
                <p>Goals: ${maxGoals}</p>
                `;

                const pens = document.getElementById('pens');
                pens.innerHTML = `
                <p>Penalties: ${playerScore[topScorerName][1]}</p>
                `;

                const nonPens = document.getElementById('non-pens');
                nonPens.innerHTML = `
                <p>Non-Penalty Goals: ${playerScore[topScorerName][2]}</p>
                `;
        })
        .catch(error => {
            console.error('Error fetching team data:', error);
        });

    fetch('/api/pl_matches')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('upcoming-fixtures').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const upcomingMatches = data.upcoming_matches;
            const updatesMatches = data.updates_match;
            //const matchIds = data.match_ids;
            const matchIds = [12436948, 12436627, 12436975, 12437007, 12437029, 12436594, 12436602, 12436610, 12436628, 12436551, 12436562, 12436575, 12436555, 12436559]; 
            const matches = document.getElementById('matches');

            matches.innerHTML = '';
            

            upcomingMatches.forEach((match, index) => {
                const matchContainer = document.createElement('div');

                const matchElement = document.createElement('p');
                matchElement.textContent = match;

                const matchButton = document.createElement('button');
                matchButton.textContent = 'View Details';
                matchButton.setAttribute('data-match-id', matchIds[index]);

                matchButton.setAttribute('id', `matchButton-${index}`);

                matchButton.classList.add('btn', 'btn-outline-dark');

                matchButton.addEventListener('click', function(){
/*
                    const updatesCont = document.getElementById('updates');
                    updatesCont.innerHTML = '';

                    const updatesMatchContainer = document.createElement('div');
                    updatesMatchContainer.classList.add('match-details-container');

                    const scoreContainer = document.createElement('div');
                    scoreContainer.classList.add('live-score-container');

                    const scoreText = document.createElement('p');
                    scoreText.textContent = 'Live Score: ';

                    scoreText.classList.add('live-score-text')

                    const matchContent = document.createElement('h5');
                    matchContent.textContent = updatesMatches[index];

                    matchContent.classList.add('match-details-text');

                    scoreContainer.appendChild(scoreText);

                    updatesMatchContainer.appendChild(matchContent);
                    updatesCont.appendChild(updatesMatchContainer);
                    updatesCont.appendChild(scoreContainer);
*/
                })

                matchContainer.appendChild(matchElement);
                matchContainer.appendChild(matchButton);

                matches.appendChild(matchContainer);
            });
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });

    fetch('/api/pl_live_matches')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('upcoming-fixtures').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const liveMatch = data.live_match;
            const liveMatchScore = data.live_match_score;

            const updatesContainer = document.getElementById('updates-cont');
            updatesContainer.innerHTML = `
            <h5 class="match-title">${liveMatch}</h5>
            <p class="match-score">${liveMatchScore}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });
    }
)

/*--------------------------------------------------------UCl Stats--------------------------------------------------------*/
document.getElementById('ucl-button').addEventListener('click', function(event) {
    event.preventDefault();

    fetch('/api/team_data_ucl')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('team-standings').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const teamStandings = document.getElementById('team-standings');
            teamStandings.innerHTML = `
                <p><strong>Position:</strong> ${data.position}</p>
                <p><strong>Points:</strong> ${data.points}</p>
                <p><strong>Games Played:</strong> ${data.played_games}</p>
                <p><strong>Won:</strong> ${data.won}</p>
                <p><strong>Draw:</strong> ${data.draw}</p>
                <p><strong>Lost:</strong> ${data.lost}</p>
                <p><strong>Goals For:</strong> ${data.goals_for}</p>
                <p><strong>Goals Conceded:</strong> ${data.goals_conceded}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching team data:', error);
        }); 

    fetch('/api/ucl_team_top_scorer')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('player-name').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const playerScore = data.player_score;

                let maxGoals = -Infinity;
                let topScorerName = '';

                Object.keys(playerScore).forEach(player => {
                    const goals = playerScore[player][0];
                    if (goals > maxGoals) {
                        maxGoals = goals;
                        topScorerName = player;
                    }
                });

                const topScorer = document.getElementById('player-name');
                topScorer.innerHTML = `
                <p>Team Top Scorer: ${topScorerName}</p>
                `;

                const nameParts = topScorerName.split(" ");
                const lastName = nameParts.at(-1).toLowerCase();
                const imageFileName = `${lastName}.jpg`;

                const baseImageURL = '/static/assets/players/';

                const fullImageURL = baseImageURL + imageFileName;
                document.getElementById('top-scorer-img').src = fullImageURL;

                const mostGoals = document.getElementById('goals');
                mostGoals.innerHTML = `
                <p>Goals: ${maxGoals}</p>
                `;

                const pens = document.getElementById('pens');
                pens.innerHTML = `
                <p>Penalties: ${playerScore[topScorerName][1]}</p>
                `;

                const nonPens = document.getElementById('non-pens');
                nonPens.innerHTML = `
                <p>Non-Penalty Goals: ${playerScore[topScorerName][2]}</p>
                `;
        })
        .catch(error => {
            console.error('Error fetching team data:', error);
        });

    fetch('/api/ucl_matches')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('upcoming-fixtures').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const upcomingMatches = data.upcoming_matches;
            const matches = document.getElementById('matches');

            matches.innerHTML = '';

            upcomingMatches.forEach(match => {
                const matchElement = document.createElement('p');
                matchElement.textContent = match;
                matches.appendChild(matchElement);
            });
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });

    fetch('/api/ucl_live_matches')
        .then(response => response.json())
        .then(data => {
            // If the data contains an error, display it
            if (data.error) {
                document.getElementById('upcoming-fixtures').innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const liveMatch = data.live_match;
            const liveMatchScore = data.live_match_score;

            const updatesContainer = document.getElementById('updates-cont');
            updatesContainer.innerHTML = `
            <h5 class="match-title">${liveMatch}</h5>
            <p class="match-score">${liveMatchScore}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });

    }
)



/*--------------------------------------------------------Close Buttons--------------------------------------------------------*/
document.getElementById('close-btn').addEventListener('click', function() {
    document.getElementById('team-standings').innerHTML = ``;
})

document.getElementById('cls-btn').addEventListener('click', function() {
    document.getElementById('matches').innerHTML = ``;
})


