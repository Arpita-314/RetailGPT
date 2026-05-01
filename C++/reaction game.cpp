#include <iostream> // Required for input/output operations (e.g., std::cout, std::cin)
#include <chrono>   // Required for high-resolution time measurements
#include <thread>   // Required for pausing execution (e.g., std::this_thread::sleep_for)
#include <random>   // Required for generating random numbers (e.g., std::mt19937, std::uniform_int_distribution)

// Main function where the program execution begins
int main() {
    // Seed the random number generator using a hardware-dependent random number engine
    // This provides a good source of randomness for the game's delay.
    std::random_device rd;
    // Mersenne Twister engine for generating pseudo-random numbers
    std::mt19937 gen(rd());
    // Distribution to generate random integers between 1000 and 5000 milliseconds (1-5 seconds)
    std::uniform_int_distribution<> distrib(1000, 5000);

    std::cout << "===============================" << std::endl;
    std::cout << "  REACTION TIME TESTER" << std::endl;
    std::cout << "===============================" << std::endl;
    std::cout << "Press ENTER as soon as you see 'GO!'." << std::endl;
    std::cout << "Press ENTER to start the game..." << std::endl;

    // Wait for the user to press ENTER to start the game
    std::cin.ignore(); // Clears any leftover newlines in the buffer from previous inputs
    std::cin.get();    // Waits for a single character input (ENTER key)

    // Generate a random delay between 1 and 5 seconds
    int random_delay_ms = distrib(gen);
    std::cout << "Waiting for 'GO!'..." << std::endl;

    // Pause the program for the random duration
    std::this_thread::sleep_for(std::chrono::milliseconds(random_delay_ms));

    std::cout << "GO!" << std::endl; // Signal to the user to react

    // Record the start time using high-resolution clock
    auto start_time = std::chrono::high_resolution_clock::now();

    // Wait for the user to press ENTER
    std::cin.get(); // Waits for the user's reaction

    // Record the end time
    auto end_time = std::chrono::high_resolution_clock::now();

    // Calculate the duration of the reaction in microseconds
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);

    // Convert microseconds to milliseconds for a more readable output
    double reaction_time_ms = static_cast<double>(duration.count()) / 1000.0;

    std::cout << "Your reaction time: " << reaction_time_ms << " ms" << std::endl;
    std::cout << "===============================" << std::endl;

    // Optional: Add a simple message based on reaction time (example)
    if (reaction_time_ms < 200) {
        std::cout << "Outstanding reaction!" << std::endl;
    } else if (reaction_time_ms < 300) {
        std::cout << "Great reaction!" << std::endl;
    } else if (reaction_time_ms < 400) {
        std::cout << "Good reaction!" << std::endl;
    } else {
        std::cout << "Keep practicing!" << std::endl;
    }

    std::cout << "Thank you for playing!" << std::endl;

    return 0; // Indicate successful program execution
}
