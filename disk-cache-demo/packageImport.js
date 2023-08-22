const dependencies = require('./package.json').dependencies;
const async = require('async'); // Using the `async` library to manage asynchronous operations

// Import and log each dependency
async.eachSeries(Object.keys(dependencies), async (dependency) => {
  try {
    await require(dependency);
    console.log(`Imported: ${dependency}`);
  } catch (error) {
    console.error(`Failed to import: ${dependency}`);
  }
}, (err) => {
  if (err) {
    console.error('An error occurred:', err);
  } else {
    console.log('All dependencies imported and logged.');
    process.exit(0);
  }
});

