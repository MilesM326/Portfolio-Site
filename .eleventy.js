module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy('./src/reset.css');
  eleventyConfig.addPassthroughCopy('./src/style.css');

  return {
    dir: {
      input: 'src',
      output: 'public',
    },
  };
};
