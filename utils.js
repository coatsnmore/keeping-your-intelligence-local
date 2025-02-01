const tokens = response.tokens || 0;  // Use 0 if tokens is undefined
const timeInSeconds = processTime || 1; // Avoid division by zero
const tokensPerSecond = tokens / timeInSeconds;
const ttc = calculateTTC(tokensPerSecond);

console.log(`
-------------------------------------------
Time to process request: ${timeInSeconds} seconds
Tokens: ${tokens}
Tokens/s: ${tokensPerSecond.toFixed(2)}
TTC (Time to Coffee): ${ttc.toFixed(2)}
`); 