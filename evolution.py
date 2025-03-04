import random
import json


genome = [] # [n, n+food_count] n= ediens (0/1) n+food_count = taa daudzums gramos (1-100)

food_count = 7793
nutrients_of_interest = ["E",
                         "FAT",
                         "CARB",
                         "PRO",
                         "FIB"]

target_profile ={"E": 2000,
                 "FAT": 30,
                 "CARB": 110,
                 "PRO": 80,
                 "FIB": 30}

# no atmiņas tiek ielādēts json objekts, kurā atrodas ēdienu datubāze ar to uzturvielām un to daudzumiem.
# Zemāk norādītajā formā. Katrs ēdiens masīvā ir dictionary formā.
food_data = [] #  {ID, NAME, ENERGY, PROTEIN, CARBS, FAT, FIBER}
with open("foods_nutrients.json") as file:
    food_data = json.load(file)
    
    
def population_generator(size: int, food_count: int):
    """Funkcija, kas izveido 0-to populaciju ar genomiem. Taa vaicā populacijas izmeru, 
    un pieejamo ēdienu daudzumu datubāzē(food_data masīvā)
    tā izveido n randomizētus genomus ar edienu geniem genoma robežās [0, food_count) un
    edienu daudzumu genus robežās [food_count, food_count*2).
    Lai iegutu ediena daudzumu gena, to var atrast indeksaa = ediena_gena_indekss + food_count
    Funkcija atgriež populacijas masivu ar n daudzuma genomiem"""
    population = []
    for x in range(0, size):
        genome = []
        for food in range(0, food_count):
            genome.append(random.randint(0,1)) # EDIENS JA, VAI NE
        for food_ammount in range(0,food_count):
            genome.append(random.randint(1,100)) # EDIENA DAUDZUMS GRAMOS
        population.append(genome)
    return population


def retriever(index: int, nutrient: str):
    """Funkcija, kas vaicā konkrēta ēdiena indexu un nepieciešamo uzturvielu.
    Un atgriež tās uzturvielas daudzumu konkrētajā ēdienā."""
    return float(food_data[index][nutrient])


def genome_profile(genome):
    """Tiek iesniegts genoms, un funkcija izveido visu genoma edienu uzturvielu daudzuma profilu katrai uzturvielai
    masiivaa nutrients_of_interest. Tiek atgriezts profils dictionary veidaa, kur katrai uzturvielai atbilst taas daudzums,
    kads bija sastopams visa genoma edienos kopaa. """
    profile = {}
    for nutrient in nutrients_of_interest:
            profile[nutrient] = 0
    for index in range(0,food_count): #food_count = genome/2
        if genome[index] == 1:
            for nutrient in nutrients_of_interest:
                profile[nutrient] += retriever(index, nutrient)*genome[index+food_count]/100 # reizinu tapec, ka katram produktam ir ari savs svars svars ir gramos, tapec dalu ar 100. maksimalais ir 100g produktam, tapec dalot ar simts maksimalais reizinatajs bus 1.
    return profile


def profile_evaluator(profile: dict):
    """Tiek iesniegts konkreta genoma uzturvielu daudzuma profils katrai uzturvielai. resp cik daudz no katras uzturvielas.
    Daudzums tiek izveerteets salidzinot ar TARGET uzturvielas daudzumu un katrai uzturvielai profilā tiek dots verteejums no 0 lidz 1 atbilstibas veidā.
    1 ir totala atbilstiba, 0 ir totala neatbilstiba. visbiezak bus kautkur starp 0 un 1. Tiek atgriezts saads dictionary profils ar vertejumiem katrai uzturvielai."""
    eval_profile = {}
    for nutrient in nutrients_of_interest:
        if profile[nutrient] < target_profile[nutrient]:
            match_value = profile[nutrient] / target_profile[nutrient]
            eval_profile[nutrient] = match_value
            print(eval_profile[nutrient])
        elif profile[nutrient] > target_profile[nutrient]:
            match_value = target_profile[nutrient] / profile[nutrient]
            eval_profile[nutrient] = match_value
        elif profile[nutrient] == target_profile[nutrient]:
            eval_profile[nutrient] = 1
        # z = abs(profile[nutrient] - target_profile[nutrient])
        # z = target_profile[nutrient] - z
        # match_value = z / target_profile[nutrient] # if target_profile[nutrient] != 0
        # # cik es galva izdomaju, ta ir procentuala atbilstiba manam target_profile. Var but gan deficita atbilstiba gan parmeriga atbilstiba. sis apvieno abus gadiijumus. cik apluukoju.
        # eval_profile[nutrient] = match_value
    return eval_profile


def tournament(genome1, genome2):
    """Divi genomi tiek nostaditi viens pret otru. tie sacensas katraa uzturvielu kategorija ar saviem rezultatiem
    (Kuram dota uzturviela %-tuali vairak atbilst TARGET dotās uzturvielas veertiibai. Tam, kuram vairak atbilst,
    tas dabust punktu. taads process katrai uzturvielai. Uzvar un tiek atgriezts tas, kuram beigaas vairak punktu.)"""
    gpoints_1 = 0
    gpoints_2 = 0
    eval_profile_1 = profile_evaluator(genome_profile(genome1))
    eval_profile_2 = profile_evaluator(genome_profile(genome2))
    for nutrient in nutrients_of_interest:
        if eval_profile_1[nutrient] > eval_profile_2[nutrient]:
            gpoints_1 += 1
        elif eval_profile_2[nutrient] > eval_profile_1[nutrient]:
            gpoints_2 +1
    if gpoints_1 > gpoints_2:
        return genome1
    elif gpoints_1 < gpoints_2:
        return genome2
    else:
        if random.randint(1,2) == 1: return genome1 # gadiijumaa ja stalemate
        else: return genome2 # --||--


def food_mutation(genome_0, mutation_rate: float): # mutation rate ir procentuali
    """n% iespeja , ka dotais ediena gens parmainisies uz pretejo vertibu (1 vai 0)"""
    genome = genome_0
    for gene_index in range(0, int(len(genome_0)/2)):
        if random.randint(1, 1/mutation_rate * 100) == 1: # 0.01% iespeja
            if genome_0[gene_index] == 1: # ja viens
                genome[gene_index] = 0 # tad parmainit uz nulli
            elif genome_0[gene_index] == 0: # ja nulle 
                genome[gene_index] = 1 # tad parmainit uz viens
    return genome


def food_ammount_mutation(genome_0, mutation_rate: float): # mutation rate ir procentuali
    """n% iespeja, ka dotais ediena daudzuma gens mutesies uz pilnigi randomizetu,
    jaunu vertibu gramos [1,100] gramu robežās"""
    genome = genome_0
    for gene_index in range(int(len(genome_0)/2), int(len(genome_0))): # edienu daudzums genoma sakas tad, kad beidzas visi edienu geni. Tad sakas tikpat daudz edienu daudzumu geni. Mums vajag tikai daudzumu indexus
        if random.randint(1, 1/mutation_rate * 100) == 1: # 1% iespeja
            genome[gene_index] = random.randint(1,100) # pilnigi mutejas konkreta ediena daudzums uz jaunu daudzumu
    return genome


def uniform_crossover(genome1, genome2):
    """uniform crossover gan pasiem edieniem, gan to daudzumiem. katram berna genam ir 50% iespeja
    nakt no vecaka_1 un 50% iespeja nakt no vecaka_2"""
    offspring = []
    for gene_index in range(0, len(genome1)):
        if random.randint(1,2) == 1:
            offspring.append(genome1[gene_index])
        else:
            offspring.append(genome2[gene_index])
    return offspring


def genome_total_value(genome):
    """A function that returns the sum of all nutrient values of that particular
    genome evaluated profile. """
    total_value = 0
    genome_value_profile = profile_evaluator(genome_profile(genome=genome))
    for key in genome_value_profile:
        total_value += genome_value_profile[key]
    return total_value/len(target_profile)
        
    
def find_elitists(top_x: int, population: list):
    """A function that selects the top x genomes in the given population
    and returns them in a list, also returns the remaining non_elitist_population, and the best genome of all elitists, and its value."""
    working_population = population
    elitists = []
    alpha_elitist = []
    alpha_elitist_value = 0
    while len(elitists) < top_x:
        best_value = 0
        best_genome = []
        for genome_index in range(0, len(working_population)):
            this_genome_value = genome_total_value(genome=working_population[genome_index])
            if this_genome_value > best_value:
                best_genome = working_population[genome_index]
                best_value = this_genome_value
        if len(alpha_elitist) == 0:
            alpha_elitist = best_genome
            alpha_elitist_value = best_value
        del working_population[genome_index]
        elitists.append(best_genome)
    return elitists, working_population, alpha_elitist, alpha_elitist_value


def elitist_crossover(partners_per_elitist: int, offspring_per_partner: int, elitists: list, population:list):
    """Funkcija, kas apraksta elites pārošanās metodiku. Katrs elites genoms sapārosies ar vismaz vienu 
    citu random genomu no populācijas. Cik daudz reizes konkretajam elites genomam tas notiks, nosaka partners_per_elitist parametrs.
    Parametrs 'offspring_per_partner' nosaka cik berni elites genomam bus no katra partnera. tā tas notiks ar katru elites biedru.
    Funkcija atgriež sarakstu ar jaunajiem genomiem."""
    elite_children = []
    for elitist in elitists:
        for partner in range(0, partners_per_elitist):
            partner_genome = population[random.randint(0, len(population))-1]
            for child in range(0, offspring_per_partner):
                elite_children.append(uniform_crossover(genome1=elitist, genome2=partner_genome))
    return elite_children
            
    
def print_solution(genome, food_data: list):
    """Prints out the solution total value,
    the foods in genome and their ammounts.
    the genome nutrition profile,
    the genome nutrition profile values for each nutrient"""
    print(f"SOLUTION TOTAL VALUE: {genome_total_value(genome=genome)}\n")
    print("FOODS: \n")
    for food_index in range(0, int(len(genome)/2)):
        food = food_data[food_index]["NAME"]
        food_ammount = genome[food_index + int(len(genome)/2)-1 ]
        print(f"\t- {food} || {food_ammount}")

    print(f"\n\nNUTRIENT AMMOUNTS IN SOLUTION: \n")
    profile = genome_profile(genome=genome)
    for key in profile:
        print(f"\t- {key}: {profile[key]}")

    print(f"\n\nEACH NUTRIENT VALUE: \n")
    eval_profile = profile_evaluator(profile=profile)
    for key in eval_profile:
        print(f"\t- {key}: {eval_profile[key]}")
    print(f"SOLUTION TOTAL VALUE: {genome_total_value(genome=genome)}\n")

    
    
    
    
                
            
def run_evolution(population_size: int,
                  food_data: list,
                  food_mutation_rate: float, # In percentage terms
                  food_ammount_mutation_rate: float, # in percentage terms
                  elitists_per_population: int,
                  partners_per_elitist: int,
                  offspring_per_elitist_partner: int,
                  offspring_per_genome: int,
                  acceptable_solution_value: float, # robezaas starp 0 un 1. kur nulle ir totala neatbilstiba TARGET profilam, un 1 ir totala atbilstiba.
                  generation_limit: int,
                  ): 
    
    best_solution_value = 0
    generation_count = 0
    
    elder_population = population_generator(size=population_size, food_count=food_count)
    print(f"POPULATION {generation_count} GENERATED! ")
    child_population = []
    child_population_ringer = 50
    
    while generation_count < generation_limit:
        child_population_ringer = 0
        elitists, non_elite_population, alpha_elitist, alpha_value = find_elitists(top_x=elitists_per_population, population=elder_population)
        best_solution_value = alpha_value
        best_solution = alpha_elitist
        print(f"ELITISTS FOUND!")

        for elite_child in elitist_crossover(partners_per_elitist=partners_per_elitist,
                                            offspring_per_partner=offspring_per_elitist_partner,
                                            elitists=elitists,
                                            population=non_elite_population):
            child_population.append(elite_child)
        
        while len(child_population) < population_size:
            parent_1 = tournament(genome1=elder_population[random.randint(0, len(elder_population)-1)],
                                genome2=elder_population[random.randint(0, len(elder_population)-1)]
                                )              
            parent_2 = tournament(genome1=elder_population[random.randint(0, len(elder_population)-1)],
                                genome2=elder_population[random.randint(0, len(elder_population)-1)]
                                )
            
            for offspring in range(0, offspring_per_genome):
                child = uniform_crossover(parent_1, parent_2)
                child = food_mutation(genome_0=child, mutation_rate=food_mutation_rate)
                child = food_ammount_mutation(genome_0=child, mutation_rate=food_ammount_mutation_rate)
                child_population.append(child)
            
            if len(child_population) >= child_population_ringer:
                print(f"CHILD GENERATION SIZE: {child_population_ringer}")
                child_population_ringer += 50
            
            
        elder_population = child_population
        child_population = []
        generation_count += 1
        print(f"GENERATION: {generation_count}")
        print_solution(best_solution, food_data=food_data)
        if best_solution_value >= acceptable_solution_value:
            print("ACCEPTABLE SOLUTION FOUND!\n")
            print_solution(best_solution, food_data=food_data)
            break
        
    
    
    
        
    
run_evolution(population_size=1000,
                food_data=food_data,
                food_mutation_rate=0.01,
                food_ammount_mutation_rate=1,
                elitists_per_population=1,
                partners_per_elitist=5,
                offspring_per_elitist_partner=4,
                offspring_per_genome=2,
                acceptable_solution_value=0.5,
                generation_limit=25000)
    
    

    
        
    
    



# TODO TODO TODO tiek genereta x populacija. tiek palaista elitists(bet elite buutu jaanonjem no parastaas populaacijas) un elitist_crossover funkcija un pievienoti pirmie jaunie genomi y populacija. Tad turpinaas parasto genomu  paarosanaas.
#                Tiek random izveleti random  2 genomi no populacijas un tournament veida 1 iznak cauri, bridi noglabats atmiņa, tad atkartojas velviens tournament process un iznak velviens cauri,
#                Talak notiek crossover starp siem diviem un 2 berni pievienoti y populacija. atkartojas tik ilgi lidz piepildaas jaunaa populaacija. un viss sis atkaartojas ar jauno populaaciju n reizes tikai 
#                tiek mainits starp x un y populacijam.

    # fn elitism, kas panem n top vertejuma genus no populacijas. Vai ari genus kuri parsit kautkadu noteiktu slieksni ( bet sis varetu paleninat programmu )
    
        