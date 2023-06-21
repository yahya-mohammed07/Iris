#ifndef CPPLIB_HPP
#define CPPLIB_HPP

#include <string>
#include <random>

inline std::string
random_choice(const std::vector<std::string> &choices) noexcept {
  std::random_device device{}; // will be used to obtain a seed for the random number engine
  const std::seed_seq seed{ // seed with a real random value, if available 
      device(), device(), device(), device(), device(),
      device(), device(), device(), device(), device(),
  };
  std::mt19937 generator{seed}; // mt19937 is a standard mersenne_twister_engine
  std::uniform_int_distribution<> distribution(0, choices.size() - 1);// define the range [0 - 6]
  return choices[distribution(generator)];
}

#endif // CPPLIB_HPP