<?php

namespace App\Http\Controllers\API\V1;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Http\Resources\V1\FeeListResource;
use App\Models\FeeList;

class FeeListController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return FeeListResource::collection(FeeList::with('city')->get());
    }

    /**
     * Display the specified resource with a foreign key.
     */
    public function showFK(string $id)
    {
        return FeeListResource::collection(FeeList::where('city_id', $id)->with('city')->get());
    }

    /**
     * Display the specified resource.
     */
    public function show(FeeList $feeList)
    {
        return new FeeListResource($feeList);
    }

}
