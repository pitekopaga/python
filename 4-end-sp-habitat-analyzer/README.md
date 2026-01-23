Endangered Species Habitat Connectivity Analyzer

(Leverages: Forestry Masters + Conservation work + GIS skills)

What it does:



Analyzes habitat fragmentation for endangered species



Uses public GIS/satellite data to identify critical corridors



Simulates impact of development projects on species mobility



Generates conservation priority maps for NGOs/government agencies



Technical Implementation:



python

class HabitatConnectivityAnalyzer:

&nbsp;   def analyze\_species\_movement(self, species, region):

&nbsp;       # Get habitat data from public APIs

&nbsp;       habitat\_data = get\_habitat\_maps(species)

&nbsp;       

&nbsp;       # Analyze fragmentation using graph theory

&nbsp;       connectivity\_graph = build\_habitat\_graph(habitat\_data)

&nbsp;       

&nbsp;       # Identify critical corridors at risk

&nbsp;       critical\_corridors = find\_bottlenecks(connectivity\_graph)

&nbsp;       

&nbsp;       # Simulate development impacts

&nbsp;       threat\_analysis = simulate\_threats(

&nbsp;           corridors=critical\_corridors,

&nbsp;           planned\_projects=get\_development\_plans(region)

&nbsp;       )

&nbsp;       

&nbsp;       # Generate conservation recommendations

&nbsp;       return ConservationReport(

&nbsp;           priority\_areas=critical\_corridors,

&nbsp;           restoration\_suggestions=suggest\_corridor\_restoration(),

&nbsp;           policy\_recommendations=generate\_policy\_brief(threat\_analysis)

&nbsp;       )







Leverage conservation work: OTS/Wilson Botanical Garden partnerships



Technical showcase: Graph algorithms + GIS + data visualization



Social impact: Direct application to real environmental problems



Portfolio piece: Shows you can build tools for environmental NGOs

