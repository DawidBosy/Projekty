
#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <time.h>
#include <vector>
#include <math.h>
using namespace sf;


int windowWidth = 1260;
int windowHeight = 720;

RenderWindow window(VideoMode(windowWidth, windowHeight), "Platformer");
View view(Vector2f(0.0f, 0.0f), Vector2f(windowWidth, windowHeight));


float accelGravity = 0.7;
float maxGravity =15;
float scaling;
int coinsLeft = 5;

std::string screenText = "Coins left:";

class Hitbox {
public:
	float left, right, top, bot;
};


class entity : public Sprite{
public:
	Vector2f velocity, size, frameSize, framesAmount;
	Hitbox hitbox;
	std::vector <IntRect> frames;
	virtual void setTex(Texture& t)= 0;
	virtual void setHitbox(float X, float Y) = 0;
};


class Coin : public virtual entity {
public:
	Coin(float X, float Y, float W, float H) {
		size.x = W;
		size.y = H;

		collected = 0;

		setHitbox(X, Y);
		setPosition(X, Y);
	};

	void setHitbox(float X, float Y) {
		hitbox.left = X + 4*scaling;
		hitbox.right = X + size.x - 4*scaling;
		hitbox.top = Y + -1*scaling;
		hitbox.bot = Y + size.y - 6*scaling;
	}

	void setTex(Texture& t) {
		setScale(scaling, scaling);
		setTexture(t);
	}
	bool collected;
};

class Platform : public virtual entity {
public:
	Platform(float X, float Y, float W, float H) {
		size.x = W;
		size.y = H;


		setHitbox(X, Y);
		setPosition(X, Y);
	};

	void setTex(Texture& t) {
		setScale(scaling, scaling);
		setTexture(t);
	}

	void setHitbox(float X, float Y) {
		hitbox.left = X + 0;
		hitbox.right = X + size.x - 0;
		hitbox.top = Y + 0;
		hitbox.bot = Y + size.y - 0;
	}
};



class Player : public virtual entity {
private:
	float speed;
	bool collision;
	bool onGround;
	float jumpHeight;
	int walkCounter, idleCounter, walkFrames, idleFrames, walkSpeed, idleSpeed;
public:
	Player(float X, float  Y, float W, float H) {


		walkCounter = 0;
		idleCounter = 0;
		walkFrames = 3;
		idleFrames = 2;
		walkSpeed = 9;
		idleSpeed = 15;


		speed = 6;
		jumpHeight = 20;
		size.x = W;
		size.y = H;


		setHitbox(X,Y);
		setPosition(X, Y);
	}


	void setTex(Texture& t) {
		frameSize.x = 16;
		frameSize.y = 16;

		framesAmount.x = t.getSize().x / frameSize.x;
		framesAmount.y = t.getSize().y / frameSize.y;
		for (int y = 0;y < framesAmount.y;y++) {
			for (int x = 0;x < framesAmount.x;x++) {
				IntRect frame(x * frameSize.x, y * frameSize.y, frameSize.x, frameSize.y);
				frames.push_back(frame);
			}
		}
		setTextureRect(frames[0]);
		setScale(scaling, scaling);
		setTexture(t);
	}

	void setHitbox(float X, float Y) {}

	void update(bool keyW, bool keyS, bool keyA, bool keyD, std::vector <Platform>& level, std::vector <Coin>& CGroup) {
		if (keyW && onGround) velocity.y = jumpHeight*-1;

		if (onGround==false) {
			velocity.y += accelGravity;
			if (velocity.y > maxGravity) velocity.y = maxGravity;
		}

		if (keyA) velocity.x = -1;
		if (keyD) velocity.x = 1;
		if (!(keyA || keyD)) velocity.x = 0;

		move(velocity.x * speed, 0);
		collide(velocity.x ,0,level);

		onGround = 0;
		move(0,velocity.y);
		collide(0, velocity.y, level);


		coinCollide(velocity.x, velocity.y, CGroup);
		animate();
	}

private:
	void collide(float xvel,float yvel, std::vector <Platform>& level) {
		for (Platform& p : level) {
			if (getPosition().x+8 < p.hitbox.right &&
				getPosition().x+size.x-4 > p.hitbox.left &&
				getPosition().y+0 < p.hitbox.bot &&
				getPosition().y+size.y > p.hitbox.top) {
				collision = 1;
			}
			else {
				collision = 0;
			}
			if (collision) {
				if (xvel > 0) {
					setPosition(p.hitbox.left - size.x + 4, getPosition().y);
					velocity.x = 0;
				}
				if (xvel < 0) { 
					setPosition(p.hitbox.right - 8, getPosition().y);
					velocity.x = 0;
				}
				if (yvel > 0) {
					setPosition(getPosition().x,p.hitbox.top - size.y + 0);
					velocity.y = 0;
					onGround = 1;
				}
				if (yvel < 0) {
					setPosition(getPosition().x, p.hitbox.bot - 0);
					velocity.y = 0;
				}
			}
		}
	}

	void coinCollide(float xvel, float yvel, std::vector<Coin>& CGroup) {
		for (Coin& p : CGroup) {
			if (getPosition().x + 8 < p.hitbox.right &&
				getPosition().x + size.x - 4 > p.hitbox.left &&
				getPosition().y < p.hitbox.bot &&
				getPosition().y + size.y > p.hitbox.top && p.collected == 0) {
				p.collected=1;
				coinsLeft--;
			}
		}
	}


	void animate() {
		if (abs(velocity.y) > 0 && velocity.x > 0) {
			setOrigin({ getLocalBounds().width, 0 });
			setScale({ -4, 4 });
			jump();
		}
		else if (abs(velocity.y) > 0 && velocity.x < 0) {
			setOrigin({ getLocalBounds().width - 16, 0 });
			setScale({ 4, 4 });
			jump();
		}
		else if (abs(velocity.y) > 0 && velocity.x == 0) {
			jump();
		}
		else if (velocity.x > 0 ) {
			setOrigin({getLocalBounds().width, 0 });
			setScale({ -4, 4 });
			walk();
		}
		else if (velocity.x < 0 ) {
			setOrigin({ getLocalBounds().width-16, 0 });
			setScale({ 4, 4 });
			walk();
		}
		else
			idle();
	}

	void walk() {
		for (int i = 0;i < walkFrames;i++) {
			if (walkCounter == (i + 1) * walkSpeed) {
				setTextureRect(frames[i]);
			}
		}
		if (walkCounter == walkFrames * walkSpeed)
			walkCounter = 0;
		walkCounter++;
	}
	void jump() {
		setTextureRect(frames[walkFrames + idleFrames]);
	}

	void idle() {
		for (int i = 0;i < idleFrames;i++) {
			if (idleCounter == (i + 1) * idleSpeed) {
				setTextureRect(frames[i+walkFrames]);
			}
		}
		if (idleCounter == idleFrames * idleSpeed)
			idleCounter = 0;
		idleCounter++;
	}

};

class Level {
public:
	std::vector <Platform> platforms;
	std::vector <Coin> coins;
	Text coinCounter;
	Font consolasFont;
	int playerStartX, playerStartY, coinMeter;
	Level() {
		consolasFont.loadFromFile("assets/fonts/BRLNSB.TTF");
		coinCounter.setCharacterSize(50);
		coinCounter.setFillColor(Color::Black);
		coinCounter.setFont(consolasFont);
	};
	void setLevel(int &CoinsLeft,int levelArray[30][30], Texture& platformTex, Texture& coinTex, int X, int Y){

		Scaling(4);
		for (int i = 0;i < 30;i++) {
			for (int j = 0;j < 30;j++) {
				if (levelArray[i][j] == 1) {
					Platform p(j * 16 * scaling, i * 16 * scaling, 16 * scaling, 16 * scaling);
					p.setTex(platformTex);
					platforms.push_back(p);
				}
				if (levelArray[i][j] == 2) {
					Coin c(j * 16 * scaling, i * 16 * scaling, 16 * scaling, 16 * scaling);
					c.setTex(coinTex);
					coins.push_back(c);
				}
			}
		}
		calcCoins(CoinsLeft);
		Prepare(X, Y);

	}

	void calcCoins(int &coinsLeft) {
		coinMeter = coins.size();
		for (Coin& p : coins) {
			if (p.collected == 1) {
				coinMeter--;
			}
		}
		coinsLeft = coinMeter;
	}

	void setText(int coinsLeft){
		if (coinsLeft > 0) {
			screenText = "Coins left: ";
			screenText.append(std::to_string(coinsLeft));
			coinCounter.setString(screenText);
		}
		else {
			coinCounter.setString("Congratulations! You collected all coins!");
		}
	}
	void Prepare(int x, int y) {
		playerStartX = x;
		playerStartY = y;
		view.zoom(1);
		window.setFramerateLimit(60);
	}
	void Scaling(int scale) {
		scaling = scale;
		for (Platform& p : platforms) {
			p.setScale(scaling,scaling);
		}
		for (Coin& p : coins) {
			p.setScale(scaling, scaling);
		}
	}
	void calcCounter(int x, int w, int y, int h) {
		coinCounter.setPosition(x + w / 2 - windowWidth / 2, y + h / 2 - windowHeight / 2);
	}
};


int main() {

	bool keyW, keyS, keyA, keyD;

	Level TestLvl;
	TestLvl.Prepare(80,1090);

	Texture playerTex;
	Texture platformsTex;
	Texture coinTex;

	playerTex.loadFromFile("assets/images/Player move.png");
	platformsTex.loadFromFile("assets/images/Grass3.png");
	coinTex.loadFromFile("assets/images/Coin.png");
	
	int levelArray[30][30] = {  {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
								{1,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,2,1},
								{1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1},
								{1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1},//10
								{1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,1},
								{1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,1,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,1,0,1,0,1},
								{1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},//20
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1},
								{1,2,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,1,1,1,0,0,0,1},
								{1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,2,0,1},
								{1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1},
								{1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1} };//30

	TestLvl.setLevel(coinsLeft, levelArray, platformsTex, coinTex, 80, 1900);



	Player player(TestLvl.playerStartX, TestLvl.playerStartY, 16*scaling, 16*scaling);
	player.setTex(playerTex);






	while (window.isOpen()) {
		Event event;
		while (window.pollEvent(event))
		{
			if (event.type == Event::Closed)
				window.close();
		}


		TestLvl.setText(coinsLeft);

		keyW = Keyboard::isKeyPressed(Keyboard::W);
		keyS = Keyboard::isKeyPressed(Keyboard::S);
		keyA = Keyboard::isKeyPressed(Keyboard::A);
		keyD = Keyboard::isKeyPressed(Keyboard::D);

		player.update(keyW, keyS, keyA, keyD, TestLvl.platforms, TestLvl.coins);


		view.setCenter(player.getPosition().x + player.size.x / 2, player.getPosition().y + player.size.y / 2);

		window.setView(view);


		window.clear(Color(10,108,188));
		



		for (Platform& p: TestLvl.platforms) {
			window.draw(p);
		}
		for (Coin& p : TestLvl.coins) {
			if (p.collected == 0) {
				window.draw(p);
			}
		}

		window.draw(player);

		TestLvl.calcCounter(player.getPosition().x,player.size.x, player.getPosition().y,player.size.y);
		window.draw(TestLvl.coinCounter);
		window.display();

	}
}