package cos418_hw1_1

import (
	"fmt"
	"sort"
	"strings"
	"regexp"
	"bufio"
	"os"
)

// Find the top K most common words in a text document.
// 	path: location of the document
//	numWords: number of words to return (i.e. k)
//	charThreshold: character threshold for whether a token qualifies as a word,
//		e.g. charThreshold = 5 means "apple" is a word but "pear" is not.
// Matching is case insensitive, e.g. "Orange" and "orange" is considered the same word.
// A word comprises alphanumeric characters only. All punctuation and other characters
// are removed, e.g. "don't" becomes "dont".
// You should use `checkError` to handle potential errors.
func topWords(path string, numWords int, charThreshold int) []WordCount {
	// TODO: implement me
	// HINT: You may find the `strings.Fields` and `strings.ToLower` functions helpful
	// HINT: To keep only alphanumeric characters, use the regex "[^0-9a-zA-Z]+"
	file, err := os.Open(path)
	checkError(err)
	defer file.Close()

	wordFreq = make(map[string]int)
	re := regexp.MustComplie('[^0-9a-zA-Z]+')
	scanner := bufio.NewScanner(file)
	for scanner.Scan(){

		line := scanner.Text()
		words := strings.Fields(strings.ToLower(re.ReplaceAllString(line, "")))

		for _, word := range words {
			if len(word) >= charThreshold {
				wordFreq[word]++
			}
		}
	}
	checkError(scanner.Err())

	var wordCounts []WordCount
	for word, count := range wordFreq{
		wordCounts = append (wordCounts, WordCount{Word: word, Count: count})
	}

	sortWordCounts(wordCounts)

	if numWords > length(wordCounts){

		return wordCounts
	}
	return wordCounts[:numWords]
}
// Helper function to handle errors
func checkError(err error) {
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
// A struct that represents how many times a word is observed in a document
type WordCount struct {
	Word  string
	Count int
}

func (wc WordCount) String() string {
	return fmt.Sprintf("%v: %v", wc.Word, wc.Count)
}

// Helper function to sort a list of word counts in place.
// This sorts by the count in decreasing order, breaking ties using the word.
// DO NOT MODIFY THIS FUNCTION!
func sortWordCounts(wordCounts []WordCount) {
	sort.Slice(wordCounts, func(i, j int) bool {
		wc1 := wordCounts[i]
		wc2 := wordCounts[j]
		if wc1.Count == wc2.Count {
			return wc1.Word < wc2.Word
		}
		return wc1.Count > wc2.Count
	})
}
func main() {
	// Call the topWords function with:
	// - "Mydocument.txt" as the file path
	// - 5 as the number of top words to display
	// - 3 as the minimum word length to consider
	topK := topWords("Mydocument.txt", 5, 3)

	// Print the results
	fmt.Println("Top words in document:")
	for _, word := range topK {
		fmt.Println(word)
	}
}
