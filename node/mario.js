import ollama from "ollama";

const progress = await ollama.pull({
  model: "tinyllama",
});

const modelfile = `
  FROM tinyllama
  SYSTEM "You are mario from super mario bros."
  `;
await ollama.create({ model: "mario", modelfile: modelfile });

const request = {
  model: "mario",
  prompt: "Who are you?",
};
const response = await ollama.generate(request);

console.log(`response: ${response.response}`);
