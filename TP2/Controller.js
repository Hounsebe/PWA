import Feed from "./Model.js";
import { render } from "./View.js";

// Fonction pour effectuer la requête fetch et récupérer les données du flux
async function fetchFeedData() {
  try {
    var userJSON = localStorage.getItem("logged");

    var user = JSON.parse(userJSON);
    const queryString = new URLSearchParams(user).toString();
    const url = `http://localhost:8000/feed?${queryString}`;
    const response = await fetch(url);
    const data = await response.json();
    return data.feed;
  } catch (error) {
    console.log("Erreur lors de la récupération des données du flux :", error);
    return [];
  }
}

// Fonction pour convertir les données du flux en objets Feed
function convertToFeeds(feedData) {
  return feedData.map((item) => {
    return new Feed(
      item.username,
      item.profil,
      item.text,
      item.image,
      item.likes
    );
  });
}

// Contrôleur principal
export async function renderFeed() {
  const feedList = await fetchFeedData();
  const feeds = convertToFeeds(feedList);

  // Appeler la fonction de rendu de la vue en passant les objets Feed
  render(feeds);
}
