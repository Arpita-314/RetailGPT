#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>

class FluidParticle {
public:
    sf::Vector2f position;
    sf::Vector2f velocity;
    float lifetime;

    FluidParticle(float x, float y) {
        position = sf::Vector2f(x, y);
        velocity = sf::Vector2f(0, 0);
        lifetime = 1.0f;
    }
};

class FluidSimulation {
private:
    std::vector<FluidParticle> particles;
    const float gravity = 9.81f;
    const float drag = 0.99f;

public:
    void addParticle(float x, float y) {
        particles.emplace_back(x, y);
    }

    void update(float deltaTime) {
        for (auto& particle : particles) {
            // Apply gravity
            particle.velocity.y += gravity * deltaTime;
            
            // Apply drag
            particle.velocity *= drag;
            
            // Update position
            particle.position += particle.velocity * deltaTime;
            
            // Decrease lifetime
            particle.lifetime -= deltaTime * 0.5f;
        }

        // Remove dead particles
        particles.erase(
            std::remove_if(particles.begin(), particles.end(),
                [](const FluidParticle& p) { return p.lifetime <= 0; }),
            particles.end());
    }

    void draw(sf::RenderWindow& window) {
        for (const auto& particle : particles) {
            sf::CircleShape shape(2);
            shape.setPosition(particle.position);
            shape.setFillColor(sf::Color(0, 128, 255, 
                static_cast<sf::Uint8>(255 * particle.lifetime)));
            window.draw(shape);
        }
    }
};

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Fluid Flow Simulation");
    window.setFramerateLimit(60);

    FluidSimulation fluid;
    sf::Clock clock;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Add particles at mouse position when left mouse button is pressed
        if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
            sf::Vector2i mousePos = sf::Mouse::getPosition(window);
            for (int i = 0; i < 5; i++) {
                fluid.addParticle(
                    mousePos.x + rand() % 10 - 5,
                    mousePos.y + rand() % 10 - 5
                );
            }
        }

        float deltaTime = clock.restart().asSeconds();
        fluid.update(deltaTime);

        window.clear(sf::Color::Black);
        fluid.draw(window);
        window.display();
    }

    return 0;
}

# Create a directory for vcpkg
cd C:\
git clone https://github.com/Microsoft/vcpkg.git

# Run the bootstrap script
C:\vcpkg\bootstrap-vcpkg.bat
C:\vcpkg\vcpkg integrate install
vcpkg install sfml:x64-windows