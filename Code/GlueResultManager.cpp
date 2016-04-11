#include <iostream> 
#include <stdio.h>
#include <sstream>
#include <string>
#include <fstream>
#include <vector>
#include <map> 
#include <utility>
#include <climits> 

using std::string;
using std::cout;
using std::cin;
using std::endl;
using std::vector; 

void Split(const std::string line, char splitter, std::vector<std::string>& vec)
{
	std::istringstream ss(line);
	std::string token;
	vec.clear();
	
	while(std::getline(ss, token, splitter)) 
	{
		vec.push_back(token);
	}	
}

class MetaRecipe
{
public: 
	bool isEven;
	int dR;
	int dx;
	int dy;
	vector<int> recipe; 
	
	bool Init(const string& line, bool even)
	{
		isEven = even;
		vector<string> vec; 
		vector<string> vals; 
		vector<string> recipeVals; 
		
		Split(line, ':', vec);
		
		if(vec.size() != 2)
			return false;
			
		Split(vec[0], ',', vals);
		
		if(vals.size() != 3)
			return false;
		
		dR = std::stoi(vals[0]);
		dx = std::stoi(vals[1]);
		dy = std::stoi(vals[2]);
		
		Split(vec[1], ',', recipeVals);
		
		recipe.clear();
		
		for(int i = 0; i < recipeVals.size(); i++)
			recipe.push_back(std::stoi(recipeVals[i]));
			
		return true;
	}
	
	void Clone(const MetaRecipe& other)
	{
		dx = other.dx;
		dy = other.dy; 
		dR = other.dR; 
		isEven = other.isEven; 
		recipe = other.recipe; 
	}
	
	bool IsNockout(const MetaRecipe& other)
	{
		if(dx == other.dx && dy == other.dy && dR >= other.dR && recipe.size() <= other.recipe.size())
			return true;
		
		return false; 
	}
	
	void Init(MetaRecipe* base, MetaRecipe* rec, int cdx, int cdy)
	{
		recipe = base->recipe;
		int delta = cdy - cdx; 
		
		for(int i = 0; i < rec->recipe.size(); i++)
			recipe.push_back(rec->recipe[i] + delta);
	}
	
	bool Update(MetaRecipe* base, MetaRecipe* rec, int cdx, int cdy)
	{
		if(recipe.size() > base->recipe.size() + rec->recipe.size())
		{
			Init(base, rec, cdx, cdy);
			return true;
		}
		
		return false;
	}
	
};

typedef vector<vector<MetaRecipe*> > RecipeMatrix;

class RecipeCollector
{
public:

	vector<RecipeMatrix> data; 
	int w_2;
	int h_2;
	
	int w; 
	int h; 
	int d; 
	
	void Init(int width, int height, int depth, bool isEven)
	{
		d = depth; 
		w = width;
		h = height;
		
		data = vector<RecipeMatrix>(depth);
		
		for(int i = 0; i < data.size(); i++)
			data[i] = vector<vector<MetaRecipe*> >(w, vector<MetaRecipe*>(h, NULL));
			
		w_2 = depth;
		h_2 = h/2;
		
		MetaRecipe* rec = new MetaRecipe();
		
		rec->Init("0,0,0:", isEven);
		
		int D = 0;
		
		if(!isEven)
			D = 1;
		
		for(int i = 0; i < data.size(); i++)
		{
			data[i][w_2][h_2 + D] = new MetaRecipe();
			data[i][w_2][h_2 + D]->Clone(*rec);
			data[i][w_2][h_2 + D]->dy += D;
		}
	}
	
	bool AddRecipe(MetaRecipe* recipe)
	{
		bool changed = false; 
		
		for(int x = 0; x < w; x++)
		{
			int cx = x + recipe->dx;
			
			if(cx < 0 || cx >= w)
				continue;
			
			for(int y = 0; y < h; y++)
			{
				int cy = y + recipe->dy;
				
				if(!recipe->isEven)
					cy--;
				
				if(cy < 0 || cy >= h)
					continue;
				
				if(((x + y) % 2 == 1 && recipe->isEven) || ((x + y) % 2 == 0 && !recipe->isEven))
					continue; 
				
				int D = 1;
				
				if(recipe->isEven)
					D = 0;
					
				int curD = -x + w_2 - recipe->dR;
				
				if(curD < 0)
					curD = 0;
				
				for(int i = curD; i < d; i++)
				{
					if(data[i][x][y] == NULL)
						continue; 
				
					if(data[i][cx][cy] == NULL)
					{
						data[i][cx][cy] = new MetaRecipe();
						data[i][cx][cy]->Init(data[i][x][y], recipe, x - w_2, y - h_2 - D);
							
						changed = true; 
					}
					else 
					{
						changed |= data[i][cx][cy]->Update(data[i][x][y], recipe, x - w_2, y - h_2 - D);
					}
				}
			}
		}
		
		return changed;
	}
	
	void Print()
	{
		for(int y = 0; y < h; y++)
		{
			for(int x = 0; x < w; x++)
			{
				if(data[d - 1][x][y] == NULL)
					cout << "X,";
				else 
					cout << data[d - 1][x][y]->recipe.size() << ",";
			}
			
			cout << "\n";
		}
		
		cout << "\n";
	}
	
	void Save(const std::string& fileName)
	{
		std::ofstream out(fileName);
		
		for(int i = 3; i < d; i++)
		{	for(int y = 5; y < h - 5; y++)
			{	for(int x = 0; x < w - 5; x++)
				{	
					if(i != 3 && i != d - 1 && -i != x - w_2)
						continue; 
					
					out << -i << ",";
					out << x - w_2 << ",";
					out << y - h_2 << ":";
					
					if(data[i][x][y] == NULL)
					{
						out << "X\n";
					}
					else 
					{
						for(int j = 0; j < data[i][x][y]->recipe.size(); j++)
						{
							out << data[i][x][y]->recipe[j];
							
							if(j < data[i][x][y]->recipe.size() - 1)
								out << ",";
						}
						
						out << "\n";
					}
				}
			}
		}
		
		out.close();
	}
};

void ReadFile(const std::string& fileName, vector<MetaRecipe*>& recipes, bool isEven)
{ 
	std::ifstream infile(fileName);
	std::string line;
	MetaRecipe metaRec; 
	
	int totalCnt = 0; 
	
	while (std::getline(infile, line))
	{
		if(!metaRec.Init(line, isEven))
			continue;
		
		bool nockedOut = false;
		 
		for(int i = 0; i < recipes.size(); i++)
		{
			if(recipes[i]->IsNockout(metaRec))
			{
				nockedOut = true;
				break;
			}
		}
		
		totalCnt++; 
		
		if(nockedOut)
			continue;
		
		MetaRecipe* newRec = new MetaRecipe();
		newRec->Clone(metaRec);
		
		recipes.push_back(newRec);
	}
	
	cout << "Total read = " << totalCnt << " , After filter = " << recipes.size() << endl;
}

bool UpdateList(vector<MetaRecipe*>& recipes, RecipeCollector& col)
{

	bool changed = false; 
	
	for(int i = 0; i < recipes.size(); i++)
		changed |= col.AddRecipe(recipes[i]);
		
	return changed; 
}
void SaveFiltered(const std::string& fileName, const vector<MetaRecipe*>& rec)
{
	std::ofstream out(fileName);
	
	for(int i = 0; i < rec.size(); i++)
	{	
		out << rec[i]->dR << ",";
		out << rec[i]->dx << ",";
		out << rec[i]->dy << ":";
		
		for(int j = 0; j < rec[i]->recipe.size(); j++)
		{
			out << rec[i]->recipe[j];
			
			if(j < rec[i]->recipe.size() - 1)
				out << ",";
		}
		
		out << "\n";
	}
	
	out.close();
}

int main()
{
	vector<MetaRecipe*> recipesEven;
	vector<MetaRecipe*> recipesOdd;
	ReadFile("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\534725[[0, 0], [1, 0], [0, 1], [1, 1]]_ValidatedEven.txt", recipesEven, true);
	ReadFile("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\534725[[0, 0], [1, 0], [0, 1], [1, 1]]_ValidatedOdd.txt", recipesOdd, false);
	
	//SaveFiltered("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\FilteredEven.txt", recipesEven);
	//SaveFiltered("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\FilteredOdd.txt", recipesOdd);
	
	/*
	for(int i = 0; i < recipesOdd.size(); i++)
	{
		if(recipesOdd[i]->dR > recipesOdd[i]->dx)
		{
			cout << "F" <<  i << "," << recipesOdd[i]->dR << "," << recipesOdd[i]->dx << "," << recipesOdd[i]->dy << ":\n";
		}
	}
	*/
	
	RecipeCollector colEven;
	RecipeCollector colOdd;
	colEven.Init(84, 240, 24, true);
	colOdd.Init(84, 240, 24, false);
	
	bool changed = true; 
	int cnt = 0; 
	
	while(changed)
	{
		changed = false;
		
		changed |= UpdateList(recipesEven, colEven);
		changed |= UpdateList(recipesOdd, colEven);
		
		changed |= UpdateList(recipesEven, colOdd);
		changed |= UpdateList(recipesOdd, colOdd);
		
		cout << cnt++ << endl;
	}
	
	colEven.Save("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\OptimizedEven.txt");
	colOdd.Save("C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\OptimizedOdd.txt");
	
	cout << "FINISH!";
	getchar();
}
