import { Item, PlayedItem } from "../types/item";
import { createWikimediaImage } from "./image";

export function formatDate(dateString: string): string{
  const date = new Date(dateString);
  // Handle invalid date strings
  //return dateString;
  console.log(dateString);
  if (isNaN(date.getTime())) {
    return "Invalid Date";
  }

  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
  const day = date.getDate().toString().padStart(2, '0');

  return `${year}-${month}-${day}`;
}

export function getRandomItem(deck: Item[], played: Item[]): Item {
  const periods: [number, number][] = [
    [-100000, 1000],
    [1000, 1800],
    [1800, 2020],
  ];
  const [fromYear, toYear] =
    periods[Math.floor(Math.random() * periods.length)];
  const avoidPeople = Math.random() > 0.5;
  const candidates = deck.filter((candidate) => {
    if (duplicate(candidate, played)) {
        console.log("duplicate");
      return false;
    }
    if (tooClose(candidate, played)) {
        console.log("too close");
      return false;
    }
    console.log("found it~");
    return true;
  });

  if (candidates.length > 0) {
    return candidates[Math.floor(Math.random() * candidates.length)];
  }
  return deck[Math.floor(Math.random() * deck.length)];
}

function tooClose(item: Item, played: Item[]) {
    console.log("checking");
  var too_close = played.some((p) => {const dateA = new Date(item.year).getTime();
                             console.log(dateA);
                             const dateB = new Date(p.year).getTime();
                             console.log(dateB);
                             return Math.abs(dateA-dateB) <= 86400000;
                            });
  console.log(too_close);
  return too_close;
}

function duplicate(item: Item, played: Item[]) {
  return played.some((p) => item.id==p.id);
}

export function checkCorrect(
  played: PlayedItem[],
  item: Item,
  index: number
): { correct: boolean; delta: number } {
  const sorted = [...played, item].sort((a, b) => {const dateA = new Date(a.year).getTime();
                                                   const dateB = new Date(b.year).getTime();
                                                   return dateA - dateB;});
  const correctIndex = sorted.findIndex((i) => {
    return i.id === item.id;
  });

  if (index !== correctIndex) {
    return { correct: false, delta: correctIndex - index };
  }

  return { correct: true, delta: 0 };
}

export function preloadImage(url: string): HTMLImageElement {
  const img = new Image();
  img.src = createWikimediaImage(url);
  return img;
}
