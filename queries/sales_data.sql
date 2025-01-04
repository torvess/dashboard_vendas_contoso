SELECT TOP 1000
	SalesKey
	,YEAR(DateKey) AS SaleYear
	,DATENAME(MONTH, DateKey) AS SaleMonth
	,DAY(DateKey) as SaleDay
	,CAST(DateKey AS DATE) AS SaleDate
	,e.ChannelName
	,c.SalesTerritoryCountry
	,c.SalesTerritoryRegion
	,c.SalesTerritoryName
	,d.CityName
	,b.StoreType
	,b.StoreName
	,h.ProductCategoryName
	,g.ProductSubcategoryName
	,f.ClassName
	,f.BrandName
	,f.ProductName
	,TotalCost
	,SalesQuantity
	,SalesAmount
	,DiscountQuantity
	,DiscountAmount
	,ReturnQuantity
	,ReturnAmount	
FROM
	FactSales a
LEFT JOIN DimStore b
	ON a.StoreKey = b.StoreKey
LEFT JOIN DimSalesTerritory c
	ON b.GeographyKey = c.GeographyKey
LEFT JOIN DimGeography d
	ON b.GeographyKey = d.GeographyKey
LEFT JOIN DimChannel e
	ON a.channelKey = e.ChannelKey
LEFT JOIN DimProduct f
	ON a.ProductKey = f.ProductKey
LEFT JOIN DimProductSubcategory g
	ON f.ProductSubcategoryKey = g.ProductSubcategoryKey
LEFT JOIN DimProductCategory h
	ON g.ProductCategoryKey = h.ProductCategoryKey